import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import math 
import threading
import mediapipe as mp

class RefApp(tk.Tk):
    def __init__(self, size):
        # main setup
        super().__init__()
        self.title('Reference Application')
        self.geometry(f"{size[0]}x{size[1]}")
        
        #styles
        self.styles()

        #side_flag
        self.current_patient = 'None'
        self.side_state = {'Right': 0, 'Left':0}
        self.frame_numbers_insole = {'Left': {}, 'Right': {}}

        # Title Frame
        self.title_frame = Side_Cam(self, self.style)
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

class Side_Cam(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=10)
        self.rowconfigure(2, weight=1)
        
        self.assessment_state_text = 'None'
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.recording = False
        self.out = None
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        # Frames
        self.top_frame = ttk.Frame(self)
        self.webcam_frame = ttk.Frame(self)
        
        self.top_frame.grid(row=0, column=0, sticky='nsew')
        self.webcam_frame.grid(row=1, column=0, sticky='nsew')

        self.record_frame = ttk.Frame(self)
        self.record_frame.grid(row=2, column=0, sticky='nsew')
        self.record_button = ttk.Button(self.record_frame, text="Start Recording", command=lambda: self.toggle_recording())
        self.record_button.pack(fill="both", expand=True)

        self.top_frame_widget()
        self.camera_update()

    def top_frame_widget(self):
        self.top_frame.rowconfigure(0, weight=1)
        self.top_frame.columnconfigure((0,1), weight=1)

        self.current_patient_label = ttk.Label(self.top_frame, text=f"Current Patient: {self.master.current_patient}", font=('Arial', 20))
        self.assessment_state_label = ttk.Label(self.top_frame, text=f"Current Video: {self.assessment_state_text}", font=('Arial', 20))

        self.current_patient_label.grid(row=0, column=0)
        self.assessment_state_label.grid(row=0, column=1)
    
    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.record_button.config(text="Stop Recording")
            
            self.output_filename = f'Data_process/Troubleshoot.mp4'
            self.out = cv2.VideoWriter(self.output_filename, self.fourcc, 10.0, (1280, 720))
            
            
        else:
            self.recording = False
            self.record_button.config(text="Start Recording")
            self.out.release()
            self.master.change_frame(self, Process_Table)
            
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

class Process_Table(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        self.style = style
        self.left_model = None
        self.right_model = None
        self.left_phase_frames = None
        self.right_phase_frames = None
        self.side_frame_numbers = {'Left': {}, 'Right': {}}
        self.image_dict = {}

        self.loading_screen = ttk.Frame(self)
        self.loading_screen.pack(fill='both', expand=True)

        self.percent_label = ttk.Label(self.loading_screen, text="", anchor='center', justify='center', font=('Arial', 24))
        self.percent_label.pack(fill='both', expand=True)

        # Start the video_to_image method in a separate thread
        threading.Thread(target=self.video_to_image).start()
    
    def video_to_image(self):

        video_path = f'Data_process/Left_sample.mp4' #video path
        output_folder = f'Data_process/Sync'
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

                        self.image_dict[frame_number] = {'Frame': frame_number,
                                                         'Image': file_path,
                                                         'Insole': '000'
                                                         }

            current_percent = int(round((frame_number / total_frames) * 100))
            self.percent_label.config(text=f"preprocessing images: {current_percent}%")
        
        # Forget the label after processing is done
        self.loading_screen.pack_forget()
        self.display_table()

        # Release resources after processing all frames
        cap.release()
        cv2.destroyAllWindows()

    def display_table(self):
        # Create a new frame for the table
        table_frame = ttk.Frame(self)
        table_frame.pack(fill='both', expand=True)

        # Create a Canvas widget to hold the labels
        canvas = tk.Canvas(table_frame)
        canvas.pack(side='left', fill='both', expand=True)

        # Create a Frame inside the canvas to hold the labels
        inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Create labels for column headings
        frame_heading = ttk.Label(inner_frame, text='Frame Number', font=('Arial', 12, 'bold'))
        frame_heading.grid(row=0, column=0, padx=5, pady=5)

        image_heading = ttk.Label(inner_frame, text='Image', font=('Arial', 12, 'bold'))
        image_heading.grid(row=0, column=1, padx=5, pady=5)

        insole_heading = ttk.Label(inner_frame, text='Insole', font=('Arial', 12, 'bold'))
        insole_heading.grid(row=0, column=2, padx=5, pady=5)

        # Populate the table using labels
        row = 1
        for frame_number, data in self.image_dict.items():
            frame_label = ttk.Label(inner_frame, text=str(data['Frame']), font=('Arial', 10))
            frame_label.grid(row=row, column=0, padx=5, pady=5)

            # Open and display the image
            img = Image.open(data['Image'])
            img = img.resize((250, 250))  # Resize image if needed
            img_tk = ImageTk.PhotoImage(img)
            image_label = ttk.Label(inner_frame, image=img_tk)
            image_label.image = img_tk  # Keep a reference to the image
            image_label.grid(row=row, column=1, padx=5, pady=5)

            insole_label = ttk.Label(inner_frame, text=str(data['Insole']), font=('Arial', 10))
            insole_label.grid(row=row, column=2, padx=5, pady=5)

            row += 1

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=canvas.yview)
        scrollbar.pack(side='right', fill='y')
        canvas.config(yscrollcommand=scrollbar.set)

        # Update canvas scroll region
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox('all'))




if __name__ == "__main__":
    app = RefApp((1920, 1080))
    app.state('zoomed')
    app.mainloop()
