import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import os
import numpy as np #better math module
import math 
from tensorflow.keras.models import load_model
import threading
import paho.mqtt.client as mqtt
import csv
import time
import mysql.connector 
import shutil #move files
from datetime import datetime #get date

mydb = mysql.connector.connect(
 	host = "localhost",
 	user= "gaitrpi",
 	password = "gait123",
 	database="gaitdata")

mycursor = mydb.cursor(buffered=True)


class RefApp(tk.Tk):
    def __init__(self, size):
        # main setup
        super().__init__()
        self.title('Reference Application')
        self.geometry(f"{size[0]}x{size[1]}")
        
        #styles
        self.styles()

        self.current_patient = 'None'
        self.current_patient_id = ''
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

        self.master.side_state = {'Right': 0, 'Left':0}

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
    
    def patient_database(self):
        #insert sql
        # global mycursor
        # mycursor.execute("SELECT name from patient_details where client_id = %s",(self.patient_entry.get(),))
        # entry_num =mycursor.fetchone()
        # if entry_num is not None:
        #     #if query returns value
            
        #     self.master.current_patient = entry_num[0]
        #     self.master.current_patient_id = self.patient_entry.get()
        #     self.master.change_frame(self, Side_Cam)
        # else:
        #     #if query returns none
        #     messagebox.showinfo("Application Database Message", "Patient not in device list, refresh or check website")
        patient_list = ['', '2400001']

        if self.patient_entry.get() in patient_list:
            self.master.current_patient = self.patient_entry.get()
            self.master.change_frame(self, Side_Cam)


        
         
        
           
          
class Side_Cam(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)

        self.assessment_state = ''
        self.assessment_state_text = 'None'

        self.esp1_sensor_data = []
        self.flag_connected = 0
        
        self.frame_number = 0
        self.nft =0
        self.pft =0
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Reduced frame width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Reduced frame height
        self.recording = False
        self.out = None

        # Frames
        self.top_frame = ttk.Frame(self)
        self.webcam_frame = ttk.Frame(self)
        self.choose_side_btn1 = ttk.Frame(self)
        
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.webcam_frame.grid(row=1, column=0, sticky='nsew')
        self.choose_side_btn1.grid(row=2, column=0, sticky='nsew')
        
        self.clear_folder('Data_process/Left_frames')
        self.clear_folder('Data_process/Right_frames')

        self.top_frame_widget()
        self.camera_thread = threading.Thread(target=self.camera_update_thread, daemon=True)
        self.camera_thread.start()
        self.choose_side_btn_widget()

    def clear_folder(self, folder_path):
        # List all items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Check if it's a file or directory
            if os.path.isfile(item_path):
                # If it's a file,  File "/home/silog/Thesis_Source_Codes/reference_app.py", line 703, in send remove it
                os.remove(item_path)

    def top_frame_widget(self):
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure((0,1), weight=1)

        self.current_patient_label = ttk.Label(self.top_frame, text=("Current Patient:"+self.master.current_patient), font=('Arial', 20))  # Changed to 'None'
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
            
            # self.right_focus_sensor()
            self.choose_side_btn1.pack_forget()
            self.assessment_state_label.config(text=f"Current Video: {self.assessment_state_text}")
            self.record_frame = ttk.Frame(self)

            self.record_frame.grid(row=2, column=0, sticky='nsew')

            self.record_label = ttk.Label(self.record_frame, text="<Space> to Start Recording")
            self.record_label.pack(fill="both", expand=True, anchor="center")

            # Bind space key to toggle recording
            self.master.bind('<space>', lambda event: self.toggle_recording(state))
            
        elif state == 'left':
            self.master.side_state['Left'] = 1
            self.assessment_state_text = 'Left'
            
            # self.left_focus_sensor()
            
            self.choose_side_btn1.pack_forget()
            self.assessment_state_label.config(text=f"Current Video: {self.assessment_state_text}")
            self.record_frame = ttk.Frame(self)

            self.record_frame.grid(row=2, column=0, sticky='nsew')

            self.record_label = ttk.Label(self.record_frame, text="<Space> to Start Recording")
            self.record_label.pack(fill="both", expand=True, anchor="center")

            # Bind space key to toggle recording
            self.master.bind('<space>', lambda event: self.toggle_recording(state))

        elif state == 'choose_other':
            if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
                self.choose_side_btn2 = ttk.Frame(self)
                self.choose_side_btn2.grid(row=2, column=0, sticky='nsew')
                # self.right_focus_sensor()
                self.choose_side_btn2.columnconfigure((0,1), weight=1)
                self.choose_side_btn2.rowconfigure(0, weight=1)

                side_btn = ttk.Button(self.choose_side_btn2, text=f"Start Left Side", command=lambda: self.change_button('left'))
                end_btn = ttk.Button(self.choose_side_btn2, text="End Video Taking", command=lambda: self.after(20, lambda: self.master.change_frame(self, Process_Table)))

                side_btn.grid(row=0, column=0, sticky='nsew')
                end_btn.grid(row=0, column=1, sticky='nsew')
            elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:
                self.choose_side_btn2 = ttk.Frame(self)
                self.choose_side_btn2.grid(row=2, column=0, sticky='nsew')
                # self.left_focus_sensor()
                self.choose_side_btn2.columnconfigure((0,1), weight=1)
                self.choose_side_btn2.rowconfigure(0, weight=1)

                side_btn = ttk.Button(self.choose_side_btn2, text=f"Start Right Side", command=lambda: self.change_button('right'))
                end_btn = ttk.Button(self.choose_side_btn2, text="End Video Taking", command=lambda: self.after(20, lambda: self.master.change_frame(self, Process_Table)))

                side_btn.grid(row=0, column=0, sticky='nsew')
                end_btn.grid(row=0, column=1, sticky='nsew')
            elif self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 1:
                self.after(20, lambda: self.master.change_frame(self, Process_Table))

    def toggle_recording(self, state):
        try:
            if not self.recording:
                self.recording = True
                self.record_label.config(text="<Space> to Stop Recording")

            else:
                self.recording = False
                self.record_label.config(text="<Space> to Start Recording")

                # Frame Number go back to 0
                self.frame_number = 0

                self.change_button('choose_other')

        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")
            # Release resources if an error occurs
            if self.out is not None:
                self.out.release()
                self.out = None
                    
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
                    # Save frame as image
                    cv2.imwrite(f'Data_process/{self.assessment_state_text}_frames/{self.frame_number}.jpg', frame)
                    
                    self.frame_number += 1
                #see current fps
                self.nft = time.time()
                self.fps = 1/(self.nft-self.pft)
                self.pft = self.nft
                self.fps = int(self.fps)
                print(self.fps)
                #see current fps end
                #self.webcam_frame.update_idletasks()
                #self.webcam_frame.update()
            
            # Schedule the next frame update
            self.webcam_frame.after(10, update_frame)  # 33 milliseconds ~= 30 fps
                        
        # Start the initial frame update
        update_frame()

    def destroy(self):
        self.cap.release()  
        super().destroy()


class Process_Table(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style
        self.left_model = []
        self.right_model = []
        self.phase_frames = []
        self.side_frame_numbers = {'Left': {}, 'Right': {}}
        self.angles_dict = {'Right': {}, 'Left': {}}
        print(f"Left: {self.master.side_state['Left']}")
        print(f"Right: {self.master.side_state['Right']}")

        self.loading_screen = ttk.Frame(self)
        self.loading_screen.pack(fill='both', expand=True)

        self.percent_label = ttk.Label(self.loading_screen, text="", anchor='center', justify='center', font=('Arial', 24))
        self.percent_label.pack(fill='both', expand=True)
        
        self.clear_folder('Data_process/Left')
        self.clear_folder('Data_process/Right')
        # Start the video_to_image method in a separate thread
        threading.Thread(target=self.video_to_image).start()

    def clear_folder(self, folder_path):
        # List all items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Check if it's a file or directory
            if os.path.isfile(item_path):
                # If it's a file,  File "/home/silog/Thesis_Source_Codes/reference_app.py", line 703, in send remove it
                os.remove(item_path)

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
        
    def crop_vid(self, side, folder_path):
        output_folder = f'Data_process/{side}'
        os.makedirs(output_folder, exist_ok=True)
        
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.8)

        total_items = len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name)) and name.endswith('.jpg')])

        for file in os.listdir(folder_path):
            if file.endswith(".jpg"):
                frame_path = os.path.join(folder_path, file)
                frame_number = int(file.split(".")[0])

                frame = cv2.imread(frame_path)
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

                            hip_angle = round(self.calculate_angle(shoulder, hip, knee), 2)
                            knee_angle = round(self.calculate_angle(hip, knee, ankle), 2)
                            ankle_angle = round(self.calculate_angle(foot_index, ankle, knee), 2)
                            self.angles_dict[side][frame_number] = {'hip': f"{hip_angle}°", 'knee': f"{knee_angle}°", 'ankle': f"{ankle_angle}°"}

                self.percent_label.config(text=f"{side} side, currently processing: {round((frame_number/total_items), 2) * 100}%")

    def video_to_image(self):
        if self.master.side_state['Right'] == 1:
            self.crop_vid('Right', 'Data_process/Right_frames')
        if self.master.side_state['Left'] == 1:
            self.crop_vid('Left', 'Data_process/Left_frames')

        # After the video processing is done, start processing images
        self.process_images()

    def process_images(self):
        # Load models for Left and Right

        if self.master.side_state['Right'] == 1:
            self.right_model = self.load_model_for_side('Right')
            self.process_images_for_side('Right', self.right_model)
        if self.master.side_state['Left'] == 1:
            self.left_model = self.load_model_for_side('Left')
            self.process_images_for_side('Left', self.left_model)
        # Switch to the table frame for further actions
        self.table_frame()

    def table_frame(self):
        # Clear existing widgets from loading_screen
        self.loading_screen.pack_forget()
        
        if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
            # Create a Combobox to select the side (Left or Right)
            self.side_var = tk.StringVar()
            self.side_var.set('Right')  # Default value
            self.side_selector = ttk.Combobox(self, textvariable=self.side_var, values=['Right'], state="readonly")
        elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:
            # Create a Combobox to select the side (Left or Right)
            self.side_var = tk.StringVar()
            self.side_var.set('Left')  # Default value
            self.side_selector = ttk.Combobox(self, textvariable=self.side_var, values=['Left'], state="readonly")
        else:
            # Create a Combobox to select the side (Left or Right)
            self.side_var = tk.StringVar()
            self.side_var.set('Left')  # Default value
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

    def send_data(self): #run ONLY ONCE
        global mycursor,mydb
        client_id = self.master.current_patient_id
        #TODO: get date, and determine if an assessment is performed before this one, if no assessment performed on date, set assessment value as 1, RUN ONCE
        date = datetime.today().strftime('%Y-%m-%d')
        print(date)
        sql = "SELECT assessment_num from assessment WHERE date_time=%s ORDER BY assessment_num DESC" #get the highest assessment number 
        val = (date,)
        mycursor.execute(sql,val)
        result = mycursor.fetchone()
        if result is not None:
            assessment_num = result[0] + 1
        else:
            assessment_num = 1
        
        #TODO: move img from data_process to Database folder, directory is as follows, RUN ONCE
        #DIR: Database/client_id/date(YYYYMMDD)/assessment_num/(Left/Right)/frame_num.jpg
        target_path = f"Database/{client_id}/{date}/{assessment_num}"
        #PS: IF directory specified does not exists, create dir
        
        #TODO: forloop this shit
        # Iterate over each row
        count = 0
        for row in self.phase_frames:
            # Extract data from the labels
            count = count + 1
            frame = row['frame_name']
            image = row['image_path']
            hips = row['rom_h']
            knees = row['rom_k']
            ankle =row['rom_a']
            insole = row['insole']
            side = row['side']
            phase_number = row['phase']
            #send data
            image =target_path+'/'+side+'/'+image
            sql = "INSERT INTO assessment (client_id, side, date_time, assessment_num, phase, image, frame, hips, knees, ankle, insole) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (client_id,side,date, assessment_num,phase_number,image,frame,hips,knees,ankle,insole)
            print(val)
            mycursor.execute(sql,val)
            
        if not os.path.exists(target_path):
            os.makedirs(target_path,exist_ok=True)
        shutil.move("Data_process/Right",target_path)
        shutil.move("Data_process/Left",target_path)
        os.makedirs('Data_process/Right', exist_ok=True)
        os.makedirs('Data_process/Left', exist_ok=True)
        print('moved files')
            
        #commit changes and close
        mydb.commit()
        print(f"sent {count} data")
        messagebox.showinfo(f"Sent data", "Data Saved")
        self.master.change_frame(self, Again)

    def load_model_for_side(self, side):
        return load_model(f'Data Inputs/models/{side}_model.h5')

    def process_images_for_side(self, side, model):
        test_data_dir = f'Data_process/{side}'
        image_files = sorted(os.listdir(test_data_dir))  # Sort the files for consistency
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
                    insole = self.master.frame_numbers_insole[side][frame_num]
                except KeyError:
                    insole = 'unknown'
                    
                rom_h = self.try_me(side,frame_num,'hip')
                rom_k = self.try_me(side,frame_num,'knee')
                rom_a = self.try_me(side,frame_num,'ankle')
                
                self.phase_frames.append({
                    'frame_name': frame_num,
                    'side': side,
                    'phase':(predicted_class+1),
                    'image_path': image_file,
                    'rom_h': rom_h,
                    'rom_k': rom_k,
                    'rom_a': rom_a,
                    'insole': insole
                })
                current_percent = int(round((index / len(image_files)) * 100))
                self.percent_label.config(text=f"{side} side, analyzing and classifying data: {current_percent}%")
    def try_me(self,side,frame_num,joint):
        try:
            angle = self.angles_dict[side][frame_num][joint]
        except KeyError:
            angle = 'Unknown'
        return angle

    def update_table(self):
        current_side = self.side_var.get()
        phase_number = int(self.phase_number_var.get())
        if current_side == 'Left':
            self.populate_table_frame(self.table_frame, 'Left', phase_number)
        else:
            self.populate_table_frame(self.table_frame, 'Right', phase_number)

    def populate_table_frame(self, table_frame, select_side, phase_number):
        # Clear existing widgets from table_frame
        for widget in table_frame.winfo_children():
            widget.destroy()

        # Define headings
        headings = ['Frame Image', 'Frame Num', 'ROM Hips', 'ROM Knees', 'ROM Ankle', 'Insole']

        # Create labels for headings with font size 20
        for col, heading in enumerate(headings):
            heading_label = tk.Label(table_frame, text=heading, font=('Helvetica', 24, 'bold'),
                                     borderwidth=1, relief='solid')
            heading_label.grid(row=0, column=col, sticky="nsew")
        
        #filter dictionary
        for x in self.phase_frames:
            print(x)
        print(f"Stored Data: {len(self.phase_frames)} entries")
        print(select_side)
        print(phase_number)
        filtered_dict = [d for d in self.phase_frames if d['side'] == select_side and d['phase'] == phase_number]
        for x in filtered_dict:
            print(x)
        print(f"Filtered Data: {len(filtered_dict)} entries")
        # Iterate over phase_frames and populate the table-like structure
        for row, frame_info in enumerate(filtered_dict):
            
            image_path = f'Data_process/{frame_info["side"]}/{frame_info["image_path"]}'
            rom_h = frame_info['rom_h']
            rom_k = frame_info['rom_k']
            rom_a = frame_info['rom_a']
            insole = frame_info['insole']
            frame_num = frame_info['frame_name']
            # Display image
            img = Image.open(image_path)
            img.thumbnail((175, 175))  # Resize image if necessary
            img = ImageTk.PhotoImage(img)
            img_label = tk.Label(table_frame, image=img, borderwidth=1, relief='solid')
            img_label.image = img  # Keep reference to avoid garbage collection
            img_label.grid(row=row, column=0, sticky="nsew")

            # Display other information with font size 20
            tk.Label(table_frame, text=frame_num, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=1, sticky="nsew")
            tk.Label(table_frame, text=rom_h, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=2, sticky="nsew")
            tk.Label(table_frame, text=rom_k, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=3, sticky="nsew")
            tk.Label(table_frame, text=rom_a, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=4, sticky="nsew")
            tk.Label(table_frame, text=insole, font=('Helvetica', 20), borderwidth=1, relief='solid').grid(row=row, column=5, sticky="nsew")
            
            # Display image
           # img2 = Image.open(insole)
           # img2.thumbnail((175, 175))  # Resize image if necessary
           # img2 = ImageTk.PhotoImage(img2)
           # img_label2 = tk.Label(table_frame, image=img2, borderwidth=1, relief='solid')
           # img_label2.image = img2  # Keep reference to avoid garbage collection
           # img_label2.grid(row=row, column=5, sticky="nsew")
            
    
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
        mydb.close() #end mydb connection
        self.master.destroy()
        

if __name__ == "__main__":
    app = RefApp((1280, 720))
    app.state('normal')
    # app.attributes('-fullscreen', True)
    app.mainloop()
