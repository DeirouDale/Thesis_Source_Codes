import customtkinter as ctk
from customtkinter import CTkImage
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import os
import cv2
import mediapipe as mp
import numpy as np
import math
import tensorflow as tf
from tensorflow.keras.models import load_model

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    width = 1280
    height = 720

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Gait Assessment System.py")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_position = (screen_width - self.width) // 2
        y_position = (screen_height - self.height) // 2

        self.geometry(f"{self.width}x{self.height}+{x_position}+{y_position}")
        self.resizable(False, False)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #mediapipe
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.imgSize = 500
        self.x_min = 0
        self.y_min = 0
        self.x_max = 0
        self.y_max = 0

        self.gait_model = load_model('model/GaitPhaseClassifier.h5')

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = ctk.CTkImage(Image.open(current_path + "/test_images/bg-sample.jpg"),size=(self.width, self.height))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image, text= '')
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = ctk.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="nse")

        #define font style- title
        self.title_style =  ctk.CTkFont(
            family = 'Raleway',
            size = 50,
            weight = 'bold'
        )

        #define font style- title
        self.subhead_style =  ctk.CTkFont(
            family = 'Montserrat',
            size = 16,
        )

        #widgets
        self.login_label = ctk.CTkLabel(self.login_frame, text="StrideSync", font= self.title_style , text_color = '#90e0ef')
        self.login_label.grid(row=0, column=0, padx=30, pady=(150, 0))
        self.login_label_sub = ctk.CTkLabel(self.login_frame, text="Gait Analysis with Computer Vision", font= self.subhead_style , text_color = '#f0f0f0')
        self.login_label_sub.grid(row=1, column=0, padx=30, pady=(0, 15))
        self.username_entry = ctk.CTkEntry(self.login_frame, width=300, placeholder_text="username", corner_radius= 20, font=('', 12), height= 35)
        self.username_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.password_entry = ctk.CTkEntry(self.login_frame, width=300, show="*", placeholder_text="password", corner_radius= 20, font=('', 12), height= 35)
        self.password_entry.grid(row=3, column=0, padx=30, pady=(0, 15))
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login_event, width= 200, font=('Montserrat', 16 ), border_spacing = 7)
        self.login_button.grid(row=4, column=0, padx=30, pady=(15, 15))


        self.login_label_sub2 = ctk.CTkLabel(self.login_frame, text="Powered by: Computer Engineering Students", font= ('Montserrat', 10 , 'italic') , text_color = '#767676')
        self.login_label_sub2.grid(row=5, column=0, padx=30, pady=(250, 15))

        
        #load and create icons for main frame
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")), dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")), dark_image=Image.open(os.path.join(image_path, "chat_light.png")), size=(20, 20))
        self.add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")), dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        self.background_frame = ctk.CTkFrame(self, corner_radius = 0, fg_color = '#f0f0f0')

        # create navigation frame
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text=" StrideSync", image=self.logo_image, compound="left", font=ctk.CTkFont(size=28, weight="bold"), text_color = '#90e0ef')
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Home",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.home_image, anchor="w" , command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 2",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.chat_image, anchor="w" , command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Frame 3",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w" , command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.back_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Log out",
            fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
            image=self.add_user_image, anchor="w" , command=self.back_event)
        self.back_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkLabel(self.home_frame, text='Gait Assessment with Computer Vision', font=ctk.CTkFont(family= 'Raleway', size = 48, weight='bold'), text_color= '#90e0ef')
        self.header.grid(row=0, column=0, padx=20, pady=(20, 0))

        self.button_frame = ctk.CTkFrame(self.home_frame, corner_radius = 0, fg_color='transparent')
        self.button_frame.grid(row = 1, column = 0)

        self.button_frame_button_1 = ctk.CTkButton(self.button_frame, text="Start Assessment", width= 300, font=('Montserrat', 16 ), border_spacing = 7, cursor= 'hand2' , command = self.camera_event)
        self.button_frame_button_1.grid(row=1, column=0, padx=20, pady=20)

        self.button_frame_button_2 = ctk.CTkButton(self.button_frame, text="Customize Settings", width= 300, font=('Montserrat', 16 ), border_spacing = 7, cursor= 'hand2')
        self.button_frame_button_2.grid(row=1, column=1, padx=20, pady=20)
        
        # create cameraframe
        self.cameraframe = ctk.CTkFrame(self.home_frame, corner_radius= 0, fg_color= 'transparent', height= 720)

        #Recording buttons
        self.button_frame_button_3 = ctk.CTkButton(self.button_frame, text="Start Recording", width= 300, font=('Montserrat', 16 ), border_spacing = 7, cursor= 'hand2' , command = self.record_event)
        self.button_frame_button_4 = ctk.CTkButton(self.button_frame, text="Finish Recording", width= 300, font=('Montserrat', 16 ), border_spacing = 7, cursor= 'hand2', state = 'disabled', command = self.stop_record_event)
        self.button_frame_button_6 = ctk.CTkButton(self.button_frame, text="Exit", width= 70, font=('Montserrat', 16 ), border_spacing = 7, cursor= 'hand2', command = self.exit_event)
        #Assessment buttons
  
        # create second frame
        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")

        #initialize the videoCapture Object
        self.cap = None 
        self.video_label = tk.Label(self.cameraframe , text= '' )
        self.video_label.configure(borderwidth=0, highlightthickness=0)
        self.video_label.pack()

        self.is_recording = False
        self.out = None

    #Login Function
    def login_event(self):
        self.login_frame.grid_forget() #remove login_frame
        self.bg_image_label.grid_forget() #remove background
        #show navigation pane
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)
        
        # select default frame
        self.select_frame_by_name("home")

    #log out Function
    def back_event(self):
        self.navigation_frame.grid_forget() #remove navigation frame()

        self.home_button.configure(fg_color="transparent")
        self.frame_2_button.configure(fg_color="transparent")
        self.frame_3_button.configure(fg_color="transparent")

        # Hide all frames
        self.home_frame.grid_forget()
        self.second_frame.grid_forget()
        self.third_frame.grid_forget()

        # Show the login frame and background image again
        self.login_frame.grid(row=0, column=0, sticky="nse")
        self.bg_image_label.grid(row=0, column=0)

    #change appearance 
    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    #navigate panels
    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    #change to home panel
    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    #camera function
    def camera_event(self):
        self.cameraframe.grid(row=2, column = 0, padx = 60, pady = 10, sticky ='nswe')

        #remove the initial buttons
        self.button_frame_button_1.grid_forget()
        self.button_frame_button_2.grid_forget()
        #show the recording buttons
        self.button_frame_button_3.grid(row=1, column=0, padx=10, pady=20)
        self.button_frame_button_6.grid(row=1, column=3, padx=10, pady=20)
        
        # Open an external webcam
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        def capture_frames():
            while True:
                # Read a frame from the webcam
                ret, frame = self.cap.read()

                # Check if the frame is read successfully
                if not ret:
                    print("Error: Could not read frame.") #currently could not read frames
                    break

                # Convert the frame from BGR to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convert the frame to a PhotoImage
                image = Image.fromarray(frame_rgb)
                photo = ImageTk.PhotoImage(image=image)

                # Update the label with the new frame
                self.video_label.configure(image=photo)
                self.video_label.image = photo

                if self.is_recording:
                    self.out.write(frame)
                
                self.after(30)


        # Start capturing frames in a separate thread
        frame_thread = Thread(target=capture_frames)
        frame_thread.start()

    def exit_event(self):
        
        #remove the recording buttons
        self.button_frame_button_3.grid_forget()
        self.button_frame_button_4.grid_forget()
        self.button_frame_button_6.grid_forget()

        #remove the cameraframe
        self.cameraframe.grid_forget()

        #show the inital buttons
        self.button_frame_button_1.grid(row=1, column=0, padx=20, pady=20)
        self.button_frame_button_2.grid(row=1, column=1, padx=20, pady=20)

        #release the webcam
        if self.cap:
            self.cap.release()

        #release the videowriter
        if self.out:
            self.out.release()
        
    def record_event(self):

        #remove the recording buttons
        self.button_frame_button_3.grid_forget()

        self.button_frame_button_4.grid(row=1, column=0, padx=10, pady=20)

        self.button_frame_button_4.configure(state = 'normal')
        self.is_recording = True
        filename = f"Video.avi"
        codec = cv2.VideoWriter_fourcc(*'XVID')
        frame_size = (int(self.cap.get(3)), int(self.cap.get(4)))
        self.out = cv2.VideoWriter(filename, codec, 20, frame_size)

    def apply_model(self, frame):
        resize = cv2.resize(frame, (256, 256))
        normalized_img = resize / 255.0
        yhat_single = self.gait_model.predict(np.expand_dims(normalized_img, axis=0))
        predicted_class = int(np.argmax(yhat_single, axis=1))
        self.prediction = ""

        if predicted_class == 0:
            self.prediction = "Phase 1"
        elif predicted_class == 1:
            self.prediction = "Phase 2"
        elif predicted_class == 2:
            self.prediction = "Phase 3"
        elif predicted_class == 3:
            self.prediction = "Phase 4"
        elif predicted_class == 4:
            self.prediction = "Phase 5"
        elif predicted_class == 5:
            self.prediction = "Phase 6"
        elif predicted_class == 6:
            self.prediction = "Phase 7"
        elif predicted_class == 7:
            self.prediction = "Phase 8"

        return self.prediction

    def analyze_video(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()

            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Process frame for pose estimation
                results = self.mp_pose_instance.process(frame_rgb)

                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark

                    left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
                    left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
                    left_foot_tip = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

                    right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
                    right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                    right_foot_tip = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

                    if all(l is not None for l in [left_hip, left_ankle, left_foot_tip, right_hip, right_ankle, right_foot_tip]):
                        self.x_min = int(min(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1])
                        self.x_max = int(max(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1])
                        self.y_min = int(min(left_hip.y, right_hip.y) * frame.shape[0])
                        self.y_max = int(max(left_ankle.y, right_ankle.y, left_foot_tip.y, right_foot_tip.y) * frame.shape[0])

                        self.x_min -= 50
                        self.y_min -= 70
                        self.x_max += 50
                        self.y_max += 60

                        self.mp_drawing.draw_landmarks(frame_rgb, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                        cv2.rectangle(frame_rgb, (self.x_min, self.y_min), (self.x_max, self.y_max), (0, 255, 0), 2)

                        bounding_box_content = frame[self.y_min:self.y_max, self.x_min:self.x_max]
                        imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255

                        if bounding_box_content.size > 0:
                            content_height, content_width, _ = bounding_box_content.shape
                            aspect_ratio = content_height / content_width

                        if aspect_ratio > 1:
                            k = self.imgSize / content_height
                            wCal = math.ceil(k * content_width)
                            imgResize = cv2.resize(bounding_box_content, (wCal, self.imgSize))
                            wGap = math.ceil((500 - wCal) / 2)
                            imgWhite[:, wGap:wCal + wGap] = imgResize
                        else:
                            k = self.imgSize / content_width
                            hCal = math.ceil(k * content_height)
                            imgResize = cv2.resize(bounding_box_content, (self.imgSize, hCal))
                            hGap = math.ceil((500 - hCal) / 2)
                            imgWhite[hGap:hCal + hGap, :] = imgResize
                
                
                            
                gait_phase = self.apply_model(imgWhite)

                text_size = cv2.getTextSize(gait_phase, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
                text_width, text_height = text_size[0], text_size[1]
                text_x = self.x_min
                text_y = self.y_max + text_height + 10 
                cv2.putText(frame_rgb, gait_phase, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                cv2.imshow("Processed Video", cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))
                cv2.imshow("Processed Video2", imgWhite)
                key = cv2.waitKey(70) & 0xFF
                if key == ord('q'):
                    break

                # image = Image.fromarray(frame_rgb)
                # photo = ImageTk.PhotoImage(image=image)

                # if hasattr(self, "video_label"):
                #     self.video_label.configure(image=photo)
                #     self.video_label.image = photo
                # else:
                #     self.video_label = tk.Label(self.cameraframe, image=photo)
                #     self.video_label.configure(borderwidth=0, highlightthickness=0)
                #     self.video_label.pack()

                # self.update_idletasks()
                # self.wait(100)

    def stop_record_event(self):
        self.button_frame_button_4.configure(state='disabled')
        if self.out:
            self.out.release()

        self.cameraframe.grid(row=2, column=0, padx=60, pady=10, sticky='nswe')

        # Remove the initial buttons
        self.button_frame_button_3.grid_forget()
        self.button_frame_button_4.grid_forget()

        # Show the recording buttons
        self.button_frame_button_6.grid(row=1, column=3, padx=10, pady=20)

        video_filename = "Video.mp4"
        self.cap = cv2.VideoCapture(video_filename)

        self.mp_pose_instance = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        # Start a separate thread to continuously show video frames and analyze
        # video_analysis_thread = Thread(target=self.analyze_video)
        # video_analysis_thread.start()
        self.analyze_video()


if __name__ == "__main__":
    app = App()
    app.mainloop()