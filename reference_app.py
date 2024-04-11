import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import os
import numpy as np
import math 
from tensorflow.keras.models import load_model
import threading
import paho.mqtt.client as mqtt
import csv


class RefApp(tk.Tk):
    def __init__(self, size):
        # main setup
        super().__init__()
        self.title('Reference Application')
        self.geometry(f"{size[0]}x{size[1]}")
        
        #styles
        self.styles()

        self.current_patient = 'None'
        self.side_state = {'Right': 0, 'Left':0}
        self.frame_numbers_insole = {'Left': {}, 'Right': {}}

        # Title Frame
        self.title_frame = Title(self, self.style)
        self.title_frame.pack(fill="both", expand=True)


    def styles(self):
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure('TButton',
                             foreground='white',
                             background='#003066',
                             font=('Arial', 18),
                             padding=[15,15,15,15]
                             )
        self.style.configure('title_box.TFrame',
                             background='orange'
                             )
        
    def change_frame(self, current_frame, next_frame_class):
        #current frame change removed
        current_frame.pack_forget()

        #new frame will show
        self.next_frame_class = next_frame_class
        self.current_frame = self.next_frame_class(self, self.style)
        self.current_frame.pack(fill='both', expand=True)
        
        if isinstance(current_frame, Side_Cam):
            current_frame.destroy()

class Title(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)

        self.style = style

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)
        
        title_frame = ttk.Frame(self, style='title_box.TFrame')
        title_frame.columnconfigure(0, weight=1)
        title_frame.rowconfigure(0, weight=2)
        title_frame.rowconfigure(1, weight=1)

        btn_frame = ttk.Frame(self)
        title_frame.grid(row=0, column=0, ipadx=150, ipady=100)
        btn_frame.grid(row=1, column=0, sticky='n')
        
        #widgets
        label_logo = ttk.Label(title_frame, text='LOGO', font=('Arial', 25), background='orange', foreground='white')
        label_title = ttk.Label(title_frame, text='Gati Assessment Device', font=('Arial', 25), background='orange', foreground='white')
        enter_btn = ttk.Button(btn_frame, text='ENTER', command=lambda: self.master.change_frame(self, Start_Assessment))

        #layout
        label_logo.grid(row=0, column=0)
        label_title.grid(row=1, column=0)
        enter_btn.pack(fill="both", expand=True)

class Start_Assessment(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)

        self.style = style

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        #frames
        self.icon_frame = ttk.Frame(self)
        self.patient_list_frame = ttk.Frame(self)

        self.icon_frame.grid(row=0, column=0, sticky='nsew')
        self.patient_list_frame.grid(row=1, column=0, sticky='nsew')

        #widgets
        self.icon_widgets()
        self.patient_list_widgets()
        enter_btn = ttk.Button(self, text='ENTER', command=self.patient_database)
        enter_btn.grid(row=2, column=0)
        
        
    def icon_widgets(self):
        
        self.icon_frame.columnconfigure((0,1), weight=1)
        self.icon_frame.rowconfigure(0, weight=1)

        internet_icon = ttk.Label(self.icon_frame, text="Internet State Icon", font=('Arial', 24))
        insole_icon = ttk.Label(self.icon_frame, text="Insole State Icon", font=('Arial', 24))

        internet_icon.grid(row=0, column=0)
        insole_icon.grid(row=0, column=1)

    def patient_list_widgets(self):

        self.patient_list_frame.columnconfigure((0,1,2), weight=1)
        self.patient_list_frame.rowconfigure(0, weight=1)

        patient_label_entry = ttk.Label(self.patient_list_frame, text='Patient Number:', font=('Arial', 24))
        self.patient_entry = ttk.Entry(self.patient_list_frame, font=('Arial', 24))

        patient_label_entry.grid(row=0, column=0)
        self.patient_entry.grid(row=0, column=1)
    
    def clear_folder(self, folder_path):
        # List all items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Check if it's a file or directory
            if os.path.isfile(item_path):
                # If it's a file, remove it
                os.remove(item_path)

    def patient_database(self):
        patient_nums = ['24-00001', '24-00002', '24-00003', '24-00004', '24-00005', '']
        entry_num = self.patient_entry.get()
        if entry_num in patient_nums:
            self.master.current_patient = entry_num
            self.clear_folder('Data_process/Left')
            self.clear_folder('Data_process/Right')
            self.master.change_frame(self, Side_Cam)
        else:
            messagebox.showinfo("Application Database Message", "Patient not in device list, refresh or check website")

class Side_Cam(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.assessment_state = 0
        self.assessment_state_text = 'None'

        self.esp1_sensor_data = []
        self.flag_connected = 0
        
        self.frame_number = 0
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Reduced frame width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Reduced frame height
        self.recording = False
        self.out = None
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        # Frames
        self.top_frame = ttk.Frame(self)
        self.webcam_frame = ttk.Frame(self)
        self.choose_side_btn1 = ttk.Frame(self)
        
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.webcam_frame.grid(row=1, column=0, sticky='nsew')
        self.choose_side_btn1.grid(row=2, column=0, sticky='nsew')

        self.top_frame_widget()
        self.camera_thread = threading.Thread(target=self.camera_update_thread, daemon=True)
        self.camera_thread.start()
        self.choose_side_btn_widget()
        
        self.client = mqtt.Client("rpi_client1") #this should be a unique name
        self.flag_connected = 0

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.message_callback_add('esp32/sensor1', self.callback_esp32_sensor1)
        self.client.message_callback_add('esp32/sensor2', self.callback_esp32_sensor2)
        self.client.message_callback_add('rpi/broadcast', self.callback_rpi_broadcast)
        self.client_subscriptions(self.client)
    #use only for mqtt here 
    def on_connect(self, client, userdata, flags, rc):
        self.flag_connected = 1
        self.client_subscriptions(self.client)
        print("Connected to MQTT server")

    def on_disconnect(self, client, userdata, rc):
        self.flag_connected = 0
        print("Disconnected from MQTT server")

        # a callback functions 
        #change from print to append

    def callback_esp32_sensor1(self, client, userdata, msg):
        print(str(msg.payload.decode('utf-8'))," ",self.frame_number)
        
        # self.esp1_sensor_data.append([str(msg.payload.decode('utf-8')),self.frame_number])

        # this is where I would save the esp data to dictionary where in the key is frame and the out is esp, example: {55: espdata}
        self.receive_insole(str(msg.payload.decode('utf-8')),self.frame_number)

    def callback_esp32_sensor2(self, client, userdata, msg):
        print('ESP sensor2 data: ', str(msg.payload.decode('utf-8')))

    def callback_rpi_broadcast(self, client, userdata, msg):
        print('RPi Broadcast message:  ', str(msg.payload.decode('utf-8')))

    def client_subscriptions(self, client):
        self.client.subscribe("esp32/#")
        self.client.subscribe("rpi/broadcast")
    #end
    def top_frame_widget(self):
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure((0,1), weight=1)

        self.current_patient_label = ttk.Label(self.top_frame, text="Current Patient: None", font=('Arial', 20))  # Changed to 'None'
        self.assessment_state_label = ttk.Label(self.top_frame, text=f"Current Video: {self.assessment_state_text}", font=('Arial', 20))

        self.current_patient_label.grid(row=0, column=0)
        self.assessment_state_label.grid(row=0, column=1)
    
    def choose_side_btn_widget(self):
        self.choose_side_btn1.columnconfigure((0,1), weight=1)
        self.choose_side_btn1.rowconfigure(0, weight=1)

        left_btn = ttk.Button(self.choose_side_btn1, text="Start Left Side", command= lambda: self.change_button('left'))
        right_btn = ttk.Button(self.choose_side_btn1, text="Start Right Side", command= lambda: self.change_button('right'))

        left_btn.grid(row=0, column=0, sticky='nsew')
        right_btn.grid(row=0, column=1, sticky='nsew')
    
    def change_button(self, state):
        self.assessment_state = state

        if state == 'right':
            self.master.side_state['Right'] = 1
            self.assessment_state_text = 'Right'

            self.choose_side_btn1.pack_forget()
            self.assessment_state_label.config(text=f"Current Video: {self.assessment_state_text}")
            self.record_frame = ttk.Frame(self)

            self.record_frame.grid(row=2, column=0, sticky='nsew')

            self.record_button = ttk.Button(self.record_frame, text="Start Recording", command=lambda: self.toggle_recording(state))
            self.record_button.pack(fill="both", expand=True)
        elif state == 'left':
            self.master.side_state['Left'] = 1
            self.assessment_state_text = 'Left'

            self.choose_side_btn1.pack_forget()
            self.assessment_state_label.config(text=f"Current Video: {self.assessment_state_text}")
            self.record_frame = ttk.Frame(self)

            self.record_frame.grid(row=2, column=0, sticky='nsew')

            self.record_button = ttk.Button(self.record_frame, text="Start Recording", command=lambda: self.toggle_recording(state))
            self.record_button.pack(fill="both", expand=True)
        elif state == 'choose_other':
            if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
                self.choose_side_btn2 = ttk.Frame(self)
                self.choose_side_btn2.grid(row=2, column=0, sticky='nsew')

                self.choose_side_btn2.columnconfigure((0,1), weight=1)
                self.choose_side_btn2.rowconfigure(0, weight=1)

                side_btn = ttk.Button(self.choose_side_btn2, text=f"Start Left Side", command=lambda: self.change_button('left'))
                end_btn = ttk.Button(self.choose_side_btn2, text="End Video Taking", command=lambda: self.master.change_frame(self, Process_Table))

                side_btn.grid(row=0, column=0, sticky='nsew')
                end_btn.grid(row=0, column=1, sticky='nsew')
            elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:
                self.choose_side_btn2 = ttk.Frame(self)
                self.choose_side_btn2.grid(row=2, column=0, sticky='nsew')

                self.choose_side_btn2.columnconfigure((0,1), weight=1)
                self.choose_side_btn2.rowconfigure(0, weight=1)

                side_btn = ttk.Button(self.choose_side_btn2, text=f"Start Right Side", command=lambda: self.change_button('right'))
                end_btn = ttk.Button(self.choose_side_btn2, text="End Video Taking", command=lambda: self.master.change_frame(self, Process_Table))

                side_btn.grid(row=0, column=0, sticky='nsew')
                end_btn.grid(row=0, column=1, sticky='nsew')
            elif self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 1:
                self.master.change_frame(self, Process_Table)

    def toggle_recording(self, state):
        try:
            if not self.recording:
                self.recording = True
                self.record_button.config(text="Stop Recording")
                
                self.client.connect('127.0.0.1',1883) # connect to mqtt
                print("connecting to mqtt")
                # start a new thread
                self.client.loop_start()
                
                if state == 1 or state == 6:
                    self.assessment_state_text = 'Left'
                elif state == 2 or state == 7:
                    self.assessment_state_text = 'Right'
                #TODO: update frame numbers here
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                output_filename = f'Data_process/{self.assessment_state_text}_vid.avi'
                self.out = cv2.VideoWriter(output_filename, fourcc, 10, (1280, 720))  # Reduced frame size

            else:
               
                self.client.disconnect() #disconnect
                self.client.loop_stop()
                self.recording = False
                self.record_button.config(text="Start Recording")

                # Frame Number go back to 0
                self.frame_number = 0

                self.change_button('choose_other')
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            # Release resources if an error occurs
            if self.out is not None:
                self.out.release()
                self.out = None

    def receive_insole(self, espdata, frame_number):
        
        if self.recording:
            if self.assessment_state == 1 or self.assessment_state == 6:
                self.master.frame_numbers_insole['Left'][frame_number] = espdata
                print(f"Left: {self.frame_number}")
                
            else:
                self.master.frame_numbers_insole['Right'][frame_number] = espdata
                print(f"Right: {self.frame_number}")
                    
    def camera_update_thread(self):
        label = ttk.Label(self.webcam_frame)
        label.grid(row=0, column=0, sticky='nsew')

        def update_frame():
            ret, frame = self.cap.read()
            if ret:
                photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                label.config(image=photo)
                label.image = photo
                
                if label.winfo_exists():
                    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                if self.recording:
                    self.out.write(frame)  
                    self.frame_number += 1

                self.webcam_frame.update_idletasks()
                self.webcam_frame.update()
            
            # Schedule the next frame update
            self.webcam_frame.after(33, update_frame)  # 33 milliseconds ~= 30 fps

        # Start the initial frame update
        update_frame()

    def destroy(self):
        self.cap.release()  
        super().destroy()

class Process_Table(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style
        self.left_model = None
        self.right_model = None
        self.left_phase_frames = None
        self.right_phase_frames = None
        self.side_frame_numbers = {'Left': {}, 'Right': {}}

        self.loading_screen = ttk.Frame(self)
        self.loading_screen.pack(fill='both', expand=True)

        self.percent_label = ttk.Label(self.loading_screen, text="", anchor='center', justify='center', font=('Arial', 24))
        self.percent_label.pack(fill='both', expand=True)

        # Start the video_to_image method in a separate thread
        threading.Thread(target=self.video_to_image).start()

    def calculate_angle(self, a, b, c):
        ab = b - a
        bc = c - b
        dot_product = np.dot(ab, bc)
        magnitude_ab = np.linalg.norm(ab)
        magnitude_bc = np.linalg.norm(bc)
        if magnitude_ab == 0 or magnitude_bc == 0:
            return None  # Avoid division by zero
        angle_radians = np.arccos(dot_product / (magnitude_ab * magnitude_bc))
        angle_degrees = np.degrees(angle_radians)

        return angle_degrees
    
    def video_to_image(self):

        angles_dict = {'Right': {}, 'Left': {}}
        side = ''

        if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
            side = 'Right'
        elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:
            side = 'Left'
        else:
            side = 'Both'

        if side == 'Right' or side == 'Left':
            video_path = f'Data_process/{side}_vid.avi' #video path
            output_folder = f'Data_process/{side}'
            os.makedirs(output_folder, exist_ok=True)

            mp_pose = mp.solutions.pose
            pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                print("Error: Could not open the video file.")
                exit()

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            for frame_number in range(1, total_frames + 1):
                ret, frame = cap.read()

                if not ret:
                    print(f"Error: Could not read frame {frame_number}.")
                    break

                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                results = pose.process(frame_rgb)

                if results.pose_landmarks:
                    mp_drawing = mp.solutions.drawing_utils
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                    landmarks = results.pose_landmarks.landmark

                    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
                    left_foot_tip = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

                    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
                    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                    right_foot_tip = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

                    if side == 'Right':
                        hip = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y])
                        knee = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y])
                        ankle = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y])
                        shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y])
                        foot_index = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y])
                    else:
                        hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y])
                        knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y])
                        ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])
                        shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y])
                        foot_index = np.array([landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y])

                    if left_hip and left_ankle and left_foot_tip and right_hip and right_ankle and right_foot_tip:
                        x_min = int(min(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1]) - 70
                        y_min = int(min(left_hip.y, right_hip.y) * frame.shape[0]) - 70
                        x_max = int(max(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1]) + 70
                        y_max = int(max(left_ankle.y, right_ankle.y, left_foot_tip.y, right_foot_tip.y) * frame.shape[0]) + 60

                        bounding_box_content = frame[y_min:y_max, x_min:x_max]

                        imgWhite = np.ones((500, 500, 3), np.uint8) * 255

                        # Resize and adjust the bounding box content
                        if bounding_box_content.size > 0:
                            content_height, content_width, _ = bounding_box_content.shape
                            aspect_ratio = content_height / content_width

                            if aspect_ratio > 1:
                                k = 500 / content_height
                                wCal = math.ceil(k * content_width)
                                imgResize = cv2.resize(bounding_box_content, (wCal, 500))
                                wGap = math.ceil((500 - wCal) / 2)
                                if imgResize.shape[1] < 500:
                                    imgWhite[:, wGap:wGap + imgResize.shape[1]] = imgResize
                                else:
                                    imgWhite[:, :] = imgResize[:, :500]
                            else:
                                k = 500 / content_width
                                hCal = math.ceil(k * content_height)
                                imgResize = cv2.resize(bounding_box_content, (500, hCal))
                                hGap = math.ceil((500 - hCal) / 2)
                                if imgResize.shape[0] < 500:
                                    imgWhite[hGap:hGap + imgResize.shape[0], :] = imgResize
                                else:
                                    imgWhite[:, :] = imgResize[:500, :]

                            file_name = f"{frame_number}.jpg"
                            file_path = os.path.join(output_folder, file_name)
                            cv2.imwrite(file_path, imgWhite)

                            #calculate and save angle of hips, knees, and ankle in a dictionary
                            hip_angle = round(self.calculate_angle(shoulder, hip, knee), 2)
                            knee_angle = round(self.calculate_angle(hip, knee, ankle), 2)
                            ankle_angle = round(self.calculate_angle(foot_index, ankle, knee), 2)
                            angles_dict[side][frame_number] = {'hip': f"{hip_angle}°", 'knee': f"{knee_angle}°", 'ankle': f"{ankle_angle}°"}

                current_percent = int(round((frame_number / total_frames) * 100))
                self.percent_label.config(text=f"{side} side, preprocessing images: {current_percent}%")
                
            # Release resources after processing each video
            cap.release()
            cv2.destroyAllWindows()
        else:
            sides = ['Right', 'Left']
            for side in sides:
                video_path = f'Data_process/{side}_vid.avi' #video path
                output_folder = f'Data_process/{side}'
                os.makedirs(output_folder, exist_ok=True)

                mp_pose = mp.solutions.pose
                pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

                cap = cv2.VideoCapture(video_path)

                if not cap.isOpened():
                    print("Error: Could not open the video file.")
                    exit()

                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                for frame_number in range(1, total_frames + 1):
                    ret, frame = cap.read()

                    if not ret:
                        print(f"Error: Could not read frame {frame_number}.")
                        break

                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    results = pose.process(frame_rgb)

                    if results.pose_landmarks:
                        mp_drawing = mp.solutions.drawing_utils
                        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                        landmarks = results.pose_landmarks.landmark

                        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
                        left_foot_tip = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

                        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
                        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                        right_foot_tip = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

                        if side == 'Right':
                            hip = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y])
                            knee = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y])
                            ankle = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y])
                            shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y])
                            foot_index = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y])
                        else:
                            hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y])
                            knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y])
                            ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])
                            shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y])
                            foot_index = np.array([landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y])

                        if left_hip and left_ankle and left_foot_tip and right_hip and right_ankle and right_foot_tip:
                            x_min = int(min(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1]) - 70
                            y_min = int(min(left_hip.y, right_hip.y) * frame.shape[0]) - 70
                            x_max = int(max(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1]) + 70
                            y_max = int(max(left_ankle.y, right_ankle.y, left_foot_tip.y, right_foot_tip.y) * frame.shape[0]) + 60

                            bounding_box_content = frame[y_min:y_max, x_min:x_max]

                            imgWhite = np.ones((500, 500, 3), np.uint8) * 255

                            # Resize and adjust the bounding box content
                            if bounding_box_content.size > 0:
                                content_height, content_width, _ = bounding_box_content.shape
                                aspect_ratio = content_height / content_width

                                if aspect_ratio > 1:
                                    k = 500 / content_height
                                    wCal = math.ceil(k * content_width)
                                    imgResize = cv2.resize(bounding_box_content, (wCal, 500))
                                    wGap = math.ceil((500 - wCal) / 2)
                                    if imgResize.shape[1] < 500:
                                        imgWhite[:, wGap:wGap + imgResize.shape[1]] = imgResize
                                    else:
                                        imgWhite[:, :] = imgResize[:, :500]
                                else:
                                    k = 500 / content_width
                                    hCal = math.ceil(k * content_height)
                                    imgResize = cv2.resize(bounding_box_content, (500, hCal))
                                    hGap = math.ceil((500 - hCal) / 2)
                                    if imgResize.shape[0] < 500:
                                        imgWhite[hGap:hGap + imgResize.shape[0], :] = imgResize
                                    else:
                                        imgWhite[:, :] = imgResize[:500, :]

                                file_name = f"{frame_number}.jpg"
                                file_path = os.path.join(output_folder, file_name)
                                cv2.imwrite(file_path, imgWhite)

                                #calculate and save angle of hips, knees, and ankle in a dictionary
                                hip_angle = round(self.calculate_angle(shoulder, hip, knee), 2)
                                knee_angle = round(self.calculate_angle(hip, knee, ankle), 2)
                                ankle_angle = round(self.calculate_angle(foot_index, ankle, knee), 2)
                                angles_dict[side][frame_number] = {'hip': f"{hip_angle}°", 'knee': f"{knee_angle}°", 'ankle': f"{ankle_angle}°"}

                    current_percent = int(round((frame_number / total_frames) * 100))
                    self.percent_label.config(text=f"{side} side, preprocessing images: {current_percent}%")
                    
                # Release resources after processing each video
                cap.release()
                cv2.destroyAllWindows()
        # After the video processing is done, start processing images
        self.process_images(angles_dict)

    def process_images(self, angles_dic):
        # Load models for Left and Right
        self.angles_dict = angles_dic

        if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
            self.right_model = self.load_model_for_side('Right')
            self.right_phase_frames = self.process_images_for_side('Right', self.right_model, self.angles_dict)
        elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:
            self.left_model = self.load_model_for_side('Left')
            self.left_phase_frames = self.process_images_for_side('Left', self.left_model, self.angles_dict)
        else:
            self.right_model = self.load_model_for_side('Right')
            self.left_model = self.load_model_for_side('Left')
            self.left_phase_frames = self.process_images_for_side('Left', self.left_model, self.angles_dict)
            self.right_phase_frames = self.process_images_for_side('Right', self.right_model, self.angles_dict)

        # Switch to the table frame for further actions
        self.table_frame()

    def table_frame(self):
        # Clear existing widgets from loading_screen
        self.loading_screen.pack_forget()

        # Create a Combobox to select the side (Left or Right)
        self.side_var = tk.StringVar()
        self.side_var.set('Left')  # Default value
        if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
            self.side_selector = ttk.Combobox(self, textvariable=self.side_var, values=['Right'], state="readonly")
        elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:
            self.side_selector = ttk.Combobox(self, textvariable=self.side_var, values=['Left'], state="readonly")
        else:
            self.side_selector = ttk.Combobox(self, textvariable=self.side_var, values=['Left', 'Right'], state="readonly")
        self.side_selector.pack()

        # Create a Combobox to select phase number
        self.phase_number_var = tk.StringVar()
        self.phase_number_var.set('1')  # Default value
        self.phase_selector = ttk.Combobox(self, textvariable=self.phase_number_var, values=[str(i) for i in range(1, 9)], state="readonly")
        self.phase_selector.pack()

        # Button to populate the table
        self.populate_button = tk.Button(self, text="Populate Table", command=self.update_table)
        self.populate_button.pack()

        # Button to send data
        self.send_button = tk.Button(self, text="Send", command=self.send_data)
        self.send_button.pack()

        # Create a canvas and attach a scrollbar to it
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')

        # Configure the canvas to utilize the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame to contain all widgets
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='center', width=1920)

        # Update scroll region when the size of the frame changes
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Make the canvas scrollable with the mouse wheel
        self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # Create a frame for the table-like structure
        self.table_frame = tk.Frame(self.scrollable_frame)
        self.table_frame.pack()

    def send_data(self):
        messagebox.showinfo("Sent data", "Data Sent to Website!")
        self.master.change_frame(self, Again)

    def load_model_for_side(self, side):
        return load_model(f'Data Inputs/models/{side}_10_Pat_New2.h5')

    def process_images_for_side(self, side, model, angles_dict):
        test_data_dir = f'Data_process/{side}'
        image_files = sorted(os.listdir(test_data_dir))  # Sort the files for consistency
        self.angles_dict = angles_dict

        # Exclude the first 10 and last 10 frames
        image_files = image_files[10:-10]

        phase_frames = {phase_num: {} for phase_num in range(1, 9)}

        for index, image_file in enumerate(image_files):
            if image_file.endswith('.jpg'):
                frame_num = int(os.path.splitext(image_file)[0])
                image_path = os.path.join(test_data_dir, image_file)
                img = cv2.imread(image_path)
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                resize = cv2.resize(img_rgb, (256, 256))
                normalized_img = resize / 255.0
                yhat_single = model.predict(np.expand_dims(normalized_img, axis=0))
                predicted_class = int(np.argmax(yhat_single, axis=1))

                # Set default values for angles if key is not found
                try:
                    rom_h = self.angles_dict[side][frame_num]['hip']
                    rom_k = self.angles_dict[side][frame_num]['knee']
                    rom_a = self.angles_dict[side][frame_num]['ankle']
                except KeyError:
                    rom_h = rom_k = rom_a = 0

                phase_frames[predicted_class + 1][frame_num] = {
                    'frame_name': f'frame {frame_num}',
                    'image_path': image_path,
                    'rom_h': rom_h,
                    'rom_k': rom_k,
                    'rom_a': rom_a,
                    'insole': 'Sample'
                }
                current_percent = int(round((index / len(image_files)) * 100))
                self.percent_label.config(text=f"{side} side, analyzing and classifying data: {current_percent}%")
        return phase_frames

    def update_table(self):
        current_side = self.side_var.get()
        phase_number = int(self.phase_number_var.get())

        if current_side == 'Left':
            self.populate_table_frame(self.table_frame, self.left_phase_frames, phase_number)
        else:
            self.populate_table_frame(self.table_frame, self.right_phase_frames, phase_number)

    def populate_table_frame(self, table_frame, phase_frames, phase_number):
        # Clear existing widgets from table_frame
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Define headings
        headings = ['Frame Image', 'ROM Hips', 'ROM Knees', 'ROM Ankle', 'Insole']

        # Create labels for headings with font size 20
        for col, heading in enumerate(headings):
            heading_label = tk.Label(table_frame, text=heading, font=('Helvetica', 24, 'bold'),
                                     borderwidth=1, relief='solid')
            heading_label.grid(row=0, column=col, sticky="nsew")

        # Iterate over phase_frames and populate the table-like structure
        for row, (frame_num, frame_info) in enumerate(phase_frames[phase_number].items(), start=1):
            image_path = frame_info['image_path']
            rom_h = frame_info['rom_h']
            rom_k = frame_info['rom_k']
            rom_a = frame_info['rom_a']
            insole = frame_info['insole']

            # Display image
            img = Image.open(image_path)
            img.thumbnail((175, 175))  # Resize image if necessary
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(table_frame, image=img, borderwidth=1, relief='solid')
            img_label.image = img  # Keep reference to avoid garbage collection
            img_label.grid(row=row, column=0, sticky="nsew")

            # Display other information with font size 20
            tk.Label(table_frame, text=rom_h, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=1, sticky="nsew")
            tk.Label(table_frame, text=rom_k, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=2, sticky="nsew")
            tk.Label(table_frame, text=rom_a, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=3, sticky="nsew")
            tk.Label(table_frame, text=insole, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=4, sticky="nsew")

class Again(ttk.Frame):
    def __init__(self, parent, style):
        '''
        Ask user if they want to assess again or not change this to your liking
        '''
        super().__init__(parent)
        self.style = style
        
        self.columnconfigure((0,2), weight=1)
        self.columnconfigure(1, minsize=5)
        self.rowconfigure(0, weight=1)

        #frames
        self.assessment_frame = ttk.Frame(self)
        border_line = ttk.Label(self, background='black')
        self.end_frame = ttk.Frame(self)
        
        self.assessment_frame.grid(row=0, column=0, sticky='nsew')
        border_line.grid(row=0, column=1, sticky='nsew')
        self.end_frame.grid(row=0, column=2, sticky='nsew')

        #widgets
        self.assessment_widgets()
        self.end_widgets()

    def assessment_widgets(self):
        
        self.assessment_frame.columnconfigure(0, weight=1)
        self.assessment_frame.rowconfigure(0, weight=2)
        self.assessment_frame.rowconfigure(1, weight=1)

        #widget
        assessment_btn = ttk.Button(self.assessment_frame, text='Assess Again', command=lambda: self.master.change_frame(self, Start_Assessment))
        #layout
        assessment_btn.grid(row=0, column=0)

    def end_widgets(self):
        self.end_frame.columnconfigure(0, weight=1)
        self.end_frame.rowconfigure(0, weight=2)
        self.end_frame.rowconfigure(1, weight=1)
        
        #widget
        end_btn = ttk.Button(self.end_frame, text='End Assessment', command=lambda: self.end_function())
        #layout
        end_btn.grid(row=0, column=0)

    def end_function(self):
        messagebox.showinfo("Clost Tab", "Thank you for using the application")
        self.master.destroy()

if __name__ == "__main__":
    app = RefApp((1280, 720))
    app.state('normal')
    # app.attributes('-fullscreen', True)
    app.mainloop()
