import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import os
import numpy as np
import math 
from tensorflow.keras.models import load_model

class RefApp(tk.Tk):
    def __init__(self, size):
        # main setup
        super().__init__()
        self.title('Reference Application')
        self.geometry(f"{size[0]}x{size[1]}")
        
        #styles
        self.styles()

        #side_flag
        self.side_flag = 'None'
        self.current_patient = 'None'

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
        self.style.map('TButton', background=[('active', '#004ea5')])
        self.style.configure('title_box.TFrame',
                             background='orange'
                             )
        
        self.style.configure('left_option.TButton',
                             foreground='white',
                             background='#003066',
                             font=('Arial', 18),
                             )
        self.style.map('left_option.TButton', background=[('active', '#004ea5')])

        self.style.configure('right_option.TButton',
                             foreground='white',
                             background='#ff6701',
                             font=('Arial', 18),
                             )
        self.style.map('right_option.TButton', background=[('active', '#ee9f27')])
        
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
        enter_btn = ttk.Button(btn_frame, text='ENTER', command=lambda: self.master.change_frame(self, LogIn))

        #layout
        label_logo.grid(row=0, column=0)
        label_title.grid(row=1, column=0)
        enter_btn.pack(fill="both", expand=True)

class LogIn(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style

        self.login_frame = tk.Frame(self)
        self.login_frame.pack()
        
        self.username_label = tk.Label(self.login_frame, text="Username: ")
        self.username_label.grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Dummy authentication, replace with your own logic
        if username == "admin" and password == "password":
            self.master.change_frame(self, Menu)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class Menu(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style
        
        self.columnconfigure((0,2), weight=1)
        self.columnconfigure(1, minsize=5)
        self.rowconfigure(0, weight=1)

        #frames
        self.assessment_frame = ttk.Frame(self)
        border_line = ttk.Label(self, background='black')
        self.monitor_frame = ttk.Frame(self)
        
        self.assessment_frame.grid(row=0, column=0, sticky='nsew')
        border_line.grid(row=0, column=1, sticky='nsew')
        self.monitor_frame.grid(row=0, column=2, sticky='nsew')

        #widgets
        self.assessment_widgets()
        self.monitor_widgets()

    def assessment_widgets(self):
        
        self.assessment_frame.columnconfigure(0, weight=1)
        self.assessment_frame.rowconfigure(0, weight=2)
        self.assessment_frame.rowconfigure(1, weight=1)

        #widget
        assessment_logo = ttk.Label(self.assessment_frame, text='ASSESSMENT LOGO', font=('Arial', 18))
        assessment_btn = ttk.Button(self.assessment_frame, text='Start Assessment', command=lambda: self.master.change_frame(self, Start_Assessment))
        #layout
        assessment_logo.grid(row=0, column=0)
        assessment_btn.grid(row=1, column=0)

    def monitor_widgets(self):
        self.monitor_frame.columnconfigure(0, weight=1)
        self.monitor_frame.rowconfigure(0, weight=2)
        self.monitor_frame.rowconfigure(1, weight=1)
        
        #widget
        monitor_logo = ttk.Label(self.monitor_frame, text='ASSESSMENT LOGO', font=('Arial', 18))
        monitor_btn = ttk.Button(self.monitor_frame, text='Monitor Data', command=lambda: print('button pressed'))
        #layout
        monitor_logo.grid(row=0, column=0)
        monitor_btn.grid(row=1, column=0)

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
        patient_refresh = ttk.Button(self.patient_list_frame, text='refresh', command=self.refresh_messagebox)

        patient_label_entry.grid(row=0, column=0)
        self.patient_entry.grid(row=0, column=1)
        patient_refresh.grid(row=0, column=2)
    
    def refresh_messagebox(self):
        messagebox.showinfo("Application Database Message", "Patient database has been synced and refreshed!")

    def patient_database(self):
        patient_nums = ['24-00001', '24-00002', '24-00003', '24-00004', '24-00005']
        entry_num = self.patient_entry.get()
        if entry_num in patient_nums:
            self.master.current_patient = entry_num
            messagebox.showinfo("Application Database Message", "Patient is in device list proceed")
            self.master.change_frame(self, Side_Cam)
        else:
            messagebox.showinfo("Application Database Message", "Patient not in device list, refresh or check website")

class Side_Cam(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)
        self.rowconfigure(2, weight=1)

        self.assessment_state = 0
        self.assessment_state_text = 'None'
        

        self.cap = cv2.VideoCapture(0)
        self.recording = False
        self.out = None

        # Frames
        self.top_frame = ttk.Frame(self)
        self.webcam_frame = ttk.Frame(self)
        self.choose_side_btn1 = ttk.Frame(self)
        

        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.webcam_frame.grid(row=1, column=0, sticky='nsew')
        self.choose_side_btn1.grid(row=2, column=0, sticky='nsew')

        self.top_frame_widget()
        self.camera_update()
        self.choose_side_btn_widget()

    def top_frame_widget(self):
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure((0,1), weight=1)

        self.current_patient_label = ttk.Label(self.top_frame, text=f"Current Patient: {self.master.current_patient}", font=('Arial', 20))
        self.assessment_state_label = ttk.Label(self.top_frame, text=f"Current Video: {self.assessment_state_text}", font=('Arial', 20))

        self.current_patient_label.grid(row=0, column=0)
        self.assessment_state_label.grid(row=0, column=1)
    
    def choose_side_btn_widget(self):
        self.choose_side_btn1.columnconfigure((0,1), weight=1)
        self.choose_side_btn1.rowconfigure(0, weight=1)

        left_btn = ttk.Button(self.choose_side_btn1, text="Start Left Side", command= lambda: self.change_button(1))
        right_btn = ttk.Button(self.choose_side_btn1, text="Start Right Side", command= lambda: self.change_button(2))

        left_btn.grid(row=0, column=0, sticky='nsew')
        right_btn.grid(row=0, column=1, sticky='nsew')
    
    def change_button(self, state):
        self.assessment_state = state
        if state == 1 or state == 2 or state == 6 or state == 7:
            
            if state == 1 or state == 6:
                self.assessment_state_text = 'Left'
            else:
                self.assessment_state_text = 'Right'

            self.choose_side_btn1.pack_forget()

            self.assessment_state_label.config(text=f"Current Video: {self.assessment_state_text}")

            self.record_frame = ttk.Frame(self)

            self.record_frame.grid(row=2, column=0, sticky='nsew')

            self.record_button = ttk.Button(self.record_frame, text="Start Recording", command=lambda: self.toggle_recording(state))
            self.record_button.pack(fill="both", expand=True)

        elif state == 3 or state == 4:
            if state == 4:
                self.assessment_state_text = 'Left'
                second_state = 6
            else:
                self.assessment_state_text = 'Right'
                second_state = 7
            self.record_button.pack_forget()

            self.choose_side_btn2 = ttk.Frame(self)
            self.choose_side_btn2.grid(row=2, column=0, sticky='nsew')

            self.choose_side_btn2.columnconfigure((0,1), weight=1)
            self.choose_side_btn2.rowconfigure(0, weight=1)

            side_btn = ttk.Button(self.choose_side_btn2, text=f"Start {self.assessment_state_text} Side", command=lambda: self.change_button(second_state))
            end_btn = ttk.Button(self.choose_side_btn2, text="End Video Taking", command=lambda: self.master.change_frame(self, Loading_screen))

            side_btn.grid(row=0, column=0, sticky='nsew')
            end_btn.grid(row=0, column=1, sticky='nsew')
        else:
            self.choose_side_btn2.pack_forget()

            self.assessment_state_label.config(text=f"Current Video: {self.assessment_state_text}")

            self.end_frame = ttk.Frame(self)

            self.end_frame.grid(row=2, column=0, sticky='nsew')

            self.end_btn = ttk.Button(self.end_frame, text="End Video Taking", command=lambda: self.master.change_frame(self, Loading_screen))
            self.end_btn.pack(fill="both", expand=True)

    def toggle_recording(self, state):
        if not self.recording:
            self.recording = True
            self.record_button.config(text="Stop Recording")
            
            if state == 1 or state == 6:
                self.assessment_state_text = 'Left'
            elif state == 2 or state == 7:
                self.assessment_state_text = 'Right'

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            output_filename = f'Data_process/{self.assessment_state_text}_vid.avi'
            self.out = cv2.VideoWriter(output_filename, fourcc, 20, (640, 480))
            
        else:
            self.recording = False
            self.record_button.config(text="Start Recording")
            self.out.release()
            if self.assessment_state == 1:
                self.change_button(3)
            elif self.assessment_state == 2:
                self.change_button(4)
            else:
                self.change_button(8)
            
    def camera_update(self):
        ret, frame = self.cap.read()

        if ret:
            photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            label = ttk.Label(self.webcam_frame, image=photo)
            label.image = photo
            label.grid(row=0, column=0, sticky='nsew')
            label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            if self.recording:
                self.out.write(frame)  
        
        self.after(20, self.camera_update)

    def destroy(self):
        self.cap.release()  
        super().destroy()

class Loading_screen(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style

        self.loading_screen = ttk.Frame(self)
        self.loading_screen.pack(fill='both', expand= True)

        loading_label = ttk.Label(self.loading_screen, text="currently analyzing video/s", anchor='center', justify='center', font=('Arial', 24)) 
        loading_label.pack(fill='both', expand=True)

        self.after(100, self.video_to_image)

        
        
    def video_to_image(self):
        sides = ['Right', 'Left']

        for side in sides:
            video_path = f'Data_process/{side}_sample.mp4'
            output_folder = f'Data_process/{side}'
            os.makedirs(output_folder, exist_ok=True)

            mp_pose = mp.solutions.pose
            pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

            cap = cv2.VideoCapture(video_path)

            ret, frame = cap.read()

            if not cap.isOpened():
                print("Error: Could not open the video file.")
                exit()
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            for frame_number in range(1, total_frames + 1):

                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)  

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

                    if left_hip and left_ankle and left_foot_tip and right_hip and right_ankle and right_foot_tip:
                        x_min = int(min(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1]) - 70
                        y_min = int(min(left_hip.y, right_hip.y) * frame.shape[0]) - 70
                        x_max = int(max(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1]) + 70
                        y_max = int(max(left_ankle.y, right_ankle.y, left_foot_tip.y, right_foot_tip.y) * frame.shape[0]) + 60

                        bounding_box_content = frame[y_min:y_max, x_min:x_max]

                        imgWhite = np.ones((500, 500, 3), np.uint8) * 255

                        if bounding_box_content.size > 0:
                            content_height, content_width, _ = bounding_box_content.shape
                            aspect_ratio = content_height / content_width

                            if aspect_ratio > 1:
                                k = 500 / content_height
                                wCal = math.ceil(k * content_width)
                                imgResize = cv2.resize(bounding_box_content, (wCal, 500))
                                wGap = math.ceil((500 - wCal) / 2)
                                imgWhite[:, wGap:wCal + wGap] = imgResize
                            else:
                                k = 500 / content_width
                                hCal = math.ceil(k * content_height)
                                imgResize = cv2.resize(bounding_box_content, (500, hCal))
                                hGap = math.ceil((500 - hCal) / 2)
                                imgWhite[hGap:hCal + hGap, :] = imgResize

                            file_name = f"{frame_number}.jpg"
                            file_path = os.path.join(output_folder, file_name)
                            cv2.imwrite(file_path, imgWhite)
                            print(f"Landmarks detected in frame {frame_number}.")
                else:
                    print(f"No landmarks detected in frame {frame_number}.")

            cap.release()
            cv2.destroyAllWindows()

        self.master.change_frame(self, Done_Analyzing)
            
    def classify_images(self):
        pass
        #create a list for left and right samples. Dont include first 15 frames and last 15 frames since these are most likely dodgy images
    
class Done_Analyzing(ttk.Frame):
     def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style

        self.done_analyzing_screen = ttk.Frame(self)
        self.done_analyzing_screen.pack(fill='both', expand=True)

        analyzed_label = ttk.Label(self.done_analyzing_screen, text="Done Analyzing", anchor='center', justify='center', font=('Arial', 24)) 
        next_btn = ttk.Button(self.done_analyzing_screen, text="Next", command=lambda: self.master.change_frame(self, Show_table))

        analyzed_label.pack(fill='both', expand=True)
        next_btn.pack(fill='both', expand=True)

class Show_table(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style

        # Define class names
        self.class_names = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5', 'Phase 6', 'Phase 7', 'Phase 8']

        # Load models for Left and Right
        left_model = self.load_model_for_side('Left')
        right_model = self.load_model_for_side('Right')

        # Process images for Left and Right
        left_phase_frames = self.process_images_for_side('Left', left_model)
        right_phase_frames = self.process_images_for_side('Right', right_model)

        # Rename images from Right side to avoid overwriting Left side images
        right_phase_frames_suffix = {}
        for phase_num, phase_data in right_phase_frames.items():
            right_phase_frames_suffix[phase_num] = {}
            for frame_num, frame_data in phase_data.items():
                if frame_num in left_phase_frames[phase_num]:
                    # Rename Right image with a suffix
                    frame_name = frame_data['frame_name']
                    frame_name_suffix = frame_name + '_right'
                    frame_data['frame_name'] = frame_name_suffix
                    right_phase_frames_suffix[phase_num][frame_num] = frame_data
                else:
                    right_phase_frames_suffix[phase_num][frame_num] = frame_data

        # Combine Left and Right phase frames
        combined_phase_frames = {}
        for phase_num in range(1, 9):
            combined_phase_frames[phase_num] = {}
            combined_phase_frames[phase_num].update(left_phase_frames[phase_num])
            combined_phase_frames[phase_num].update(right_phase_frames_suffix[phase_num])

        # Create frame for the table
        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for the table
        canvas = tk.Canvas(frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure canvas scrolling
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create another frame inside the canvas to hold the table
        table_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=table_frame, anchor="nw")

        # Populate the combined table
        self.populate_table(combined_phase_frames, table_frame)

    def load_model_for_side(self, side):
        return load_model(f'Data_collection/models/{side}_10_Pat_New2.h5')

    def process_images_for_side(self, side, model):
        test_data_dir = f'Data_process/{side}'

        image_files = os.listdir(test_data_dir)

        # Create an empty dictionary to store frame numbers for each phase, along with their frame names and images
        phase_frames = {phase_num: {} for phase_num in range(1, 9)}

        for image_file in image_files:
            if image_file.endswith('.jpg'):
                frame_num = int(os.path.splitext(image_file)[0])  # Extract frame number from the image file name

                image_path = os.path.join(test_data_dir, image_file)

                img = cv2.imread(image_path)

                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                resize = cv2.resize(img_rgb, (256, 256))

                normalized_img = resize / 255.0

                yhat_single = model.predict(np.expand_dims(normalized_img, axis=0))

                predicted_class = int(np.argmax(yhat_single, axis=1))

                # Add the frame information to the corresponding phase dictionary
                phase_frames[predicted_class + 1][frame_num] = {'frame_name': f'frame {frame_num}', 'image_path': image_path, 'phase': predicted_class}

        return phase_frames

    def show_image(self, image_path):
        # Open the image file
        image = Image.open(image_path)
        # Resize image for display
        image = image.resize((200, 200))
        # Convert Image object to Tkinter PhotoImage object
        photo = ImageTk.PhotoImage(image)
        
        return photo

    def populate_table(self, data, parent):
        # Create labels for each phase
        for col, phase_name in enumerate(self.class_names):
            ttk.Label(parent, text=phase_name).grid(row=0, column=col, padx=10)

        # Initialize counters for each phase
        phase_counters = {phase_num: 1 for phase_num in range(1, 9)}

        # Populate the table with frames for each phase
        for phase_num, phase_data in data.items():
            for frame_num, frame_data in phase_data.items():
                frame_name = frame_data['frame_name']
                image_path = frame_data['image_path']
                # Load image and convert to Tkinter PhotoImage
                photo = self.show_image(image_path)
                # Create label to display the image
                label = tk.Label(parent, image=photo, borderwidth=1, relief="solid")
                label.photo = photo  # Keep reference to prevent garbage collection
                label.grid(row=phase_counters[phase_num], column=phase_num - 1, padx=10, pady=10)
                # Create label to display frame name
                ttk.Label(parent, text=frame_name, borderwidth=1, relief="solid").grid(row=phase_counters[phase_num] + 1, column=phase_num - 1, padx=10)
                # Increment counter for the current phase
                phase_counters[phase_num] += 2  # Increment by 2 to leave space for frame name

# Example usage:
if __name__ == "__main__":
    app = RefApp((850, 540))
    app.mainloop()
