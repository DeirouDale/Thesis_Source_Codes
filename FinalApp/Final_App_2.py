import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from PIL import Image, ImageTk
import cv2
#import mediapipe as mp
import os
import numpy as np
import math 
#from tensorflow.keras.models import load_model
import threading
import customtkinter as ctk
from tkcalendar import Calendar, DateEntry

class refApp(ctk.CTk):
    def __init__(self, size):
        # main setup
        super().__init__()

        #icons
        current_path = os.path.dirname(os.path.realpath(__file__))
        #logo with name
        self.logo_image = ctk.CTkImage(Image.open(current_path + "/img/trial logo 2.png"),size= (236, 376))
        #background image
        self.bg_image = ctk.CTkImage(Image.open(current_path + "/img/bg_gradient.jpg"),size= (size[0], size[1]))
        #logo w/out name
        self.logo_image_2 = ctk.CTkImage(Image.open(current_path + "/img/trial logo.png"),size= (200, 200))

        self.iconbitmap(current_path +"/img/trial logo.ico")

        #icons dark and light
        self.logo_image_80 = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/trial logo.png")),
                                                 dark_image=Image.open(os.path.join(current_path +"/img/trial logo-light.png")), size=(80, 80))
        
        #Navigation Bar Icons
        self.assessment_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/assessment.png")),
                                                 dark_image=Image.open(os.path.join(current_path + "/img/assessment-light.png")), size=(40, 40))
        self.records_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/verify.png")),
                                                 dark_image=Image.open(os.path.join(current_path + "/img/verify-light.png")), size=(40, 40))
        self.account_user_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/users.png")),
                                                 dark_image=Image.open(os.path.join(current_path + "/img/users-light.png")), size=(25, 25))
        self.register_patient_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/patient.png")),
                                                 dark_image=Image.open(os.path.join(current_path + "/img/patient-light.png")), size=(40, 40))
        self.log_out_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/logout.png")),
                                                 dark_image=Image.open(os.path.join(current_path + "/img/logout-light.png")), size=(25, 25))
        self.patient_ID_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/patient-id.png")),
                                                 dark_image=Image.open(os.path.join(current_path + "/img/patient-id-light.png")), size=(40, 40))
        self.back_button_icon = ctk.CTkImage(light_image = Image.open(os.path.join(current_path + "/img/turn-back.png")),
                                             dark_image=Image.open(os.path.join(current_path + "/img/turn-back-light.png")), size=(40, 40))
          
        self.search_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/search.png")),
                                                 dark_image=Image.open(os.path.join(current_path + "/img/search-light.png")), size=(30, 30))
        self.delete_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/delete.png")),
                                                 dark_image=Image.open(os.path.join(current_path + "/img/delete-light.png")), size=(30, 30))
        self.eye_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/eye.png")),
                                                 dark_image=Image.open(os.path.join(current_path +"/img/eye-light.png")), size=(30, 30))
        self.calendar_icon = ctk.CTkImage(light_image=Image.open(os.path.join(current_path + "/img/calendar.png")),
                                                 dark_image=Image.open(os.path.join(current_path +"/img/calendar-light.png")), size=(30, 30))  

        self.title('Gait Insight Device')

        # Calculate the x and y coordinates for the window to be centered
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title("Gait Insight Device")

        #side_flag
        self.current_patient = 'None'
        self.popup_window = None
        self.side_state = {'Right': 0, 'Left':0}
        self.frame_numbers_insole = {'Left': {}, 'Right': {}}

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title_frame = title(self)
        self.title_frame.pack(fill="both", expand=True)
    
    def change_frame(self, current_frame, next_frame_class):
        #current frame change removed
        if isinstance(current_frame, next_frame_class):
            return
        current_frame.pack_forget()

        #new frame will show
        self.next_frame_class = next_frame_class
        self.current_frame = self.next_frame_class(self)
        self.current_frame.pack(fill='both', expand=True)
        
        if isinstance(current_frame, Side_Cam):
            current_frame.destroy()

    def open_popupWindow(self, window):
        self.window = window
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = self.window(self)
            self.popup_window.attributes('-topmost', 'true') 
        else:
            self.popup_window.focus()

    def open_popupWindow_reg(self, window, string):
        self.window = window
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = self.window(self, string)
            self.popup_window.attributes('-topmost', 'true') 
        else:
            self.popup_window.focus()

class title(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg_image_label = ctk.CTkLabel(self, image=self.master.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = ctk.CTkFrame(self, corner_radius=0, width= 520, height= 720, fg_color= "white")
        self.login_frame.grid(row=0, column=0)
        
        #create a logo
        self.logo_image_label = ctk.CTkLabel(self.login_frame, image= self.master.logo_image, text="")
        self.logo_image_label.grid(row=0, column=0, padx=80, pady=(80, 15))
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login to your Accountss", font= ctk.CTkFont(family= "Raleway", size=24, weight="bold"), text_color= "#03045e")
        self.login_label.grid(row=1, column=0, padx=80, pady=(15, 15))
        self.pin_entry = ctk.CTkEntry(self.login_frame, width=270, height= 45, placeholder_text="Pin Number", fg_color= "#d3d3d3", text_color= "black", placeholder_text_color= "black", border_color= "#FAFAFA")
        self.pin_entry.grid(row=3, column=0, padx= 80, pady=(5, 20))
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=lambda: self.master.change_frame(self, MainMenu), width=270, font= ctk.CTkFont(size= 14, weight= "bold"), height = 35)
        self.login_button.grid(row=4, column=0, padx=80, pady=(10, 80))

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        #create background image
        self.bg_image_label = ctk.CTkLabel(self, image=self.master.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        #create a Menu Frame
        self.menuFrame =ctk.CTkFrame(self, corner_radius= 0, fg_color= "white")
        self.menuFrame.grid(row=0, column=0)

        #create a title and logo
        self.logo_label = ctk.CTkLabel(self.menuFrame, image= self.master.logo_image_2, text="")
        self.title_label = ctk.CTkLabel(self.menuFrame, font= ctk.CTkFont(family= "Raleway", size = 28, weight= "bold"), text= "Navigation Menu" , text_color= "#03045e")
        self.logo_label.grid(row = 0, column = 0, padx = 80, pady = (80, 15))
        self.title_label.grid(row = 1, column = 0, padx = 80, pady=(15, 15))
        
        #assessment button
        self.assessment_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image =self.master.assessment_icon, text= "Start Assessment", 
                                               font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2",
                                                command=lambda: self.master.change_frame(self, StartAssessment))
        self.assessment_button.grid(row = 2, column = 0, padx = 80, pady = (25, 15))
 
        #records button
        self.records_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image =self.master.records_icon, text= "Patient Records", 
                                            font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2", 
                                            command=lambda: self.master.change_frame(self, patient_Records))
        self.records_button.grid(row = 3, column = 0, padx = 80, pady = (15, 15))

        #register patient button
        self.register_patient_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image =self.master.register_patient_icon, text= "Register Patient", 
                                                     font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2", 
                                                     command=lambda: self.master.change_frame(self, regPatient))
        self.register_patient_button.grid(row = 5, column = 0, padx = 80, pady = (15, 80))

class MenuBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #create Navigation Frame Icons
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        #Title
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text= "Gait Insight", image=self.master.logo_image_80, 
                                                             compound="left", font= ctk.CTkFont(size= 24, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx = 40, pady = 20)

        #start assessment button
        self.assessment_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Start Assessment",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.master.assessment_icon, anchor="center", command=lambda: self.master.change_frame(self, StartAssessment))
        self.assessment_button.grid(row=1, column=0, sticky="ew", pady=(10, 10))

        #record button
        self.record_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Patient Records",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.master.records_icon, anchor="center", command=lambda: self.master.change_frame(self, patient_Records))
        self.record_button.grid(row=2, column=0, sticky="ew", pady=(10, 10))
        
        #register patient button
        self.register_patient_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Register Patients",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.master.register_patient_icon, anchor="center", command=lambda: self.master.change_frame(self, regPatient))
        self.register_patient_button.grid(row=4, column=0, sticky="ew", pady=(10, 10))

        #account settings and Log out
        self.account_setting = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=20, border_spacing=10, text="Account Setting",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.master.account_user_icon, anchor="center", command= lambda:self.master.open_popupWindow(Account_Settings))
        self.account_setting.grid(row=6, column=0, pady=(10, 10), sticky="ews")
        
        #Log out Button
        self.Log_out = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=20, border_spacing=10, text="Log out",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.master.log_out_icon, anchor="center", command=lambda: self.master.change_frame(self, title))
        self.Log_out.grid(row=7, column=0, pady=(10, 40), sticky="ews")

class StartAssessment(MenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        #create a frame for the start Assessment
        self.start_assessment_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color= "transparent")
        self.start_assessment_frame.grid(row = 0, column = 1, pady = 50, padx = 50)
        
        self.start_assessment_frame.grid_rowconfigure(0, weight=1)
        self.start_assessment_frame.grid_columnconfigure(0, weight=1)

        #create a frame for the insole sync
        self.title_insole = ctk.CTkLabel(self.start_assessment_frame, text= "Pressure Insole Status", font= ctk.CTkFont(size=24, weight= "bold", family = "Raleway"))
        self.title_insole.grid(row = 0, column = 0)

        #create a frame for patient input and button
        self.patient_input_frame = ctk.CTkFrame(self.start_assessment_frame, corner_radius= 0, fg_color = "transparent")
        self.patient_input_frame.grid(row = 1, column = 0)

        # patient input label
        self.label_patient = ctk.CTkLabel(self.patient_input_frame, font=ctk.CTkFont(size = 18, family = "montserrat", weight= "bold"), text= "Enter the Patient ID: ")
        self.label_patient.pack(side = tk.LEFT, padx = 10, pady= 70)
        self.patient_input =ctk.CTkEntry(self.patient_input_frame, width=270, height= 40)
        self.patient_input.pack(side = tk.LEFT, padx = 10, pady= 70)
        self.patient_button = ctk.CTkButton(self.patient_input_frame, height= 40, width = 150, text= "SUBMIT", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = lambda:self.master.open_popupWindow(popupWindow))
        self.patient_button.pack(side = tk.LEFT, padx = 10, pady= 70)

class popupWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        size = [600, 400]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        #Main Info Frame
        self.info_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color="transparent") 
        self.info_frame.grid(row = 0, column= 0, padx = 20, pady = 20)

        self.warning = ctk.CTkLabel(self.info_frame, text= "Warning", font= ctk.CTkFont(size= 22, family= "raleway", weight= "bold"))
        self.warning.grid(row = 0, column = 0, pady= (20, 40))

        #Button Frames
        self.button_frame = ctk.CTkFrame(self.info_frame, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row = 3, column = 0, pady=(40, 20))
        
        self.proceed_button = ctk.CTkButton(self.button_frame, height= 40, width = 200, text= "PROCEED", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = self.proceed)
        self.proceed_button.pack(side = tk.LEFT, padx = 10)
        self.change_button = ctk.CTkButton(self.button_frame, height= 40, width = 200, text= "RETURN", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = self.go_back_to_assessment)
        self.change_button.pack(side = tk.LEFT, padx = 10)

    def proceed(self):
        self.info_frame.destroy()

        #Main Info Frame
        self.info_frame_2 = ctk.CTkFrame(self, corner_radius= 0, fg_color="transparent") 
        self.info_frame_2.grid(row = 0, column= 0, padx = 20, pady = 20)

        #title
        self.info_label = ctk.CTkLabel(self.info_frame_2, text= "Patient's Information", font= ctk.CTkFont(size= 22, family= "raleway", weight= "bold"))
        self.info_label.grid(row = 0, column = 0, pady= (20, 40))

        #Patient Info Frame
        self.patientNum_frame = ctk.CTkFrame(self.info_frame_2, corner_radius= 0, fg_color= "transparent")
        self.patientNum_frame.grid(row = 1, column = 0)
        
        self.ID_icon = ctk.CTkLabel(self.patientNum_frame, text="", image= self.master.patient_ID_icon)
        self.ID_icon.pack(side=tk.LEFT, padx = 10, pady = 20)
        
        self.patient_number = ctk.CTkLabel(self.patientNum_frame, text= "Patient's ID: ", font= ctk.CTkFont(size = 18, family= "montserrat"))
        self.patient_number.pack(side=tk.LEFT, padx = 10, pady = 20)

        self.patient_number_input = ctk.CTkLabel(self.patientNum_frame, text= "20-050146", width= 170, height = 35, font=ctk.CTkFont(size = 18, family= "montserrat", weight= "bold"))
        self.patient_number_input.pack(side=tk.LEFT, padx = 10, pady = 20)

        #Patient Name Info Frame
        self.patientName_frame = ctk.CTkFrame(self.info_frame_2, corner_radius= 0, fg_color= "transparent")
        self.patientName_frame.grid(row = 2, column = 0)
        self.patient_icon = ctk.CTkLabel(self.patientName_frame, text="", image= self.master.register_patient_icon)
        self.patient_icon.pack(side=tk.LEFT, padx = 10, pady = 20)
        self.patient_name = ctk.CTkLabel(self.patientName_frame, text= "Patient's Name: ", font= ctk.CTkFont(size = 18, family= "montserrat"))
        self.patient_name.pack(side=tk.LEFT, padx = 10, pady = 20)
        self.patient_name_input = ctk.CTkLabel(self.patientName_frame, text= "Selwyne Christian Ponce", width= 170, height = 35, font=ctk.CTkFont(size = 18, family= "montserrat", weight= "bold"))
        self.patient_name_input.pack(side=tk.LEFT, padx = 10, pady = 20)

        #Button Frames
        self.button_frame = ctk.CTkFrame(self.info_frame_2, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row = 3, column = 0, pady=(40, 20)) 
        self.proceed_button = ctk.CTkButton(self.button_frame, height= 40, width = 200, text= "PROCEED", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = self.go_to_assessment)
        self.proceed_button.pack(side = tk.LEFT, padx = 10)
        self.change_button = ctk.CTkButton(self.button_frame, height= 40, width = 200, text= "CHANGE", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = self.go_back_to_assessment)
        self.change_button.pack(side = tk.LEFT, padx = 10)
    
    def go_back_to_assessment(self):
        self.destroy()
        self.master.focus_set()
    
    def go_to_assessment(self):
        self.destroy()
        self.master.change_frame(self.master.current_frame, Side_Cam)

class Side_Cam(MenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        self.assessment_state = ''
        self.assessment_state_text = 'None'

        self.frame_number = 0
        self.nft =0
        self.pft =0
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Reduced frame width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Reduced frame height
        self.recording = False
        self.out = None

        #create a main frame
        self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color= "transparent")
        self.main_frame.grid(row = 0, column = 1, pady = 50, padx = 50)

        #create a frame for text frame
        self.text_frame = ctk.CTkFrame(self.main_frame, corner_radius = 0, fg_color = "transparent")
        self.text_frame.grid(row = 0, column = 1, pady = 20, padx = 20)

        #create a frame for web cam
        self.web_cam_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color = "transparent")
        self.web_cam_frame.grid(row = 1, column = 1, pady = 20, padx = 20)

        #create a frame for buttons
        self.choose_buttons_frame = ctk.CTkFrame(self.main_frame, corner_radius= 0, fg_color = "transparent")
        self.choose_buttons_frame.grid(row = 2, column = 1, pady = 20, padx = 20)

        #current Patient Label and Current Video
        self.current_patient = ctk.CTkLabel(self.text_frame, text = "Current Patient: None", font= ctk.CTkFont(size = 24, family = "montserrat"))
        self.current_patient.grid(row = 0, column = 1, padx = (0, 120))
        self.current_leg = ctk.CTkLabel(self.text_frame, text = f"Current Video: {self.assessment_state_text}", font= ctk.CTkFont(size = 24, family = "montserrat"))
        self.current_leg.grid(row = 0, column = 2, padx = (120, 0))

        #choose side button
        self.right_button = ctk.CTkButton(self.choose_buttons_frame, text= "START RIGHT LEG", height = 60, width = 270, 
                                          font= ctk.CTkFont(size = 18, family = "raleway", weight= "bold"),
                                          cursor = "hand2", command= lambda: self.change_button('right'))
        self.right_button.grid(row = 0, column = 0, padx = (0, 120))
        self.Left_button = ctk.CTkButton(self.choose_buttons_frame, text= "START LEFT LEG", height = 60, width = 270, 
                                          font= ctk.CTkFont(size = 18, family = "raleway", weight= "bold"),
                                          cursor = "hand2", command= lambda: self.change_button('left'))
        self.Left_button.grid(row = 0, column = 1, padx = (120, 0))

        self.camera_thread = threading.Thread(target=self.camera_update_thread, daemon=True)
        self.camera_thread.start()

        #self.client = mqtt.Client("rpi_client1") #this should be a unique name
        #self.flag_connected = 0

        ##self.client.on_connect = self.on_connect
        ##self.client.on_disconnect = self.on_disconnect
        #self.client.message_callback_add('esp32/sensor1', self.callback_esp32_sensor1)
        #self.client.message_callback_add('esp32/sensor2', self.callback_esp32_sensor2)
        #placed into left/right logic
        ##self.client.message_callback_add('rpi/broadcast', self.callback_rpi_broadcast)
        ##self.client_subscriptions(self.client)

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
    def right_focus_sensor(self):
        self.client.message_callback_add('esp32/sensor1', self.callback_esp32_sensor1)
        self.client.message_callback_remove('esp32/sensor2')
    def left_focus_sensor(self):
        self.client.message_callback_add('esp32/sensor2', self.callback_esp32_sensor2)
        self.client.message_callback_remove('esp32/sensor1')
                    
    def callback_esp32_sensor1(self, client, userdata, msg):
        print("RSensor: ",str(msg.payload.decode('utf-8'))," ",self.frame_number)
        
        # self.esp1_sensor_data.append([str(msg.payload.decode('utf-8')),self.frame_number])

        # this is where I would save the esp data to dictionary where in the key is frame and the out is esp, example: {55: espdata}
        self.receive_insole(str(msg.payload.decode('utf-8')),self.frame_number)

    def callback_esp32_sensor2(self, client, userdata, msg):
        print("LSensor: ",str(msg.payload.decode('utf-8'))," ",self.frame_number)
        self.receive_insole(str(msg.payload.decode('utf-8')),self.frame_number)
        
    def callback_rpi_broadcast(self, client, userdata, msg):
        print('RPi Broadcast message:  ', str(msg.payload.decode('utf-8')))

    def client_subscriptions(self, client):
        self.client.subscribe("esp32/#")
        self.client.subscribe("rpi/broadcast")
    #end

    def change_button(self, state):
        self.assessment_state = state

        if state == 'right':
            self.master.side_state['Right'] = 1
            self.assessment_state_text = 'Right'
            
            #self.right_focus_sensor()
            self.choose_buttons_frame.grid_forget()
            self.current_leg.configure(text=f"Current Video: {self.assessment_state_text}")

            self.record_frame = ctk.CTkFrame(self.main_frame, fg_color= "#1F6AA5")

            self.record_frame.grid(row=2, column=1)
            
            self.record_label = ctk.CTkLabel(self.record_frame, text= "Press Space to Start Recording", font = ctk.CTkFont(size = 24, family= "montserrat"))
            self.record_label.grid(row = 0, column = 0, pady = 20, padx = 460)
            
            # Bind space key to toggle recording
            self.master.bind('<space>', lambda event: self.toggle_recording(state))

        elif state == 'left':
            self.master.side_state['Left'] = 1
            self.assessment_state_text = 'Left'
            
            #self.left_focus_sensor()
            self.choose_buttons_frame.grid_forget()
            self.current_leg.configure(text=f"Current Video: {self.assessment_state_text}")

            self.record_frame = ctk.CTkFrame(self.main_frame, fg_color= "#1F6AA5")
 
            self.record_frame.grid(row=2, column=1)

            self.record_label = ctk.CTkLabel(self.record_frame, text= "Press Space to Start Recording", font = ctk.CTkFont(size = 24, family= "montserrat"))
            self.record_label.grid(row = 0, column = 0, pady = 20, padx = 460)

            # Bind space key to toggle recording
        
        elif state == 'choose_other':
            if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
                self.choose_buttons_frame_2 = ctk.CTkFrame(self.main_frame, corner_radius = 0, fg_color = "transparent" )
                self.choose_buttons_frame_2.grid(row=2, column= 1)
                #self.right_focus_sensor()

                #choose side button
                self.Left_button_2 = ctk.CTkButton(self.choose_buttons_frame_2, text= "START LEFT LEG", height = 60, width = 270, 
                                          font= ctk.CTkFont(size = 18, family = "raleway", weight= "bold"),
                                          cursor = "hand2", command= lambda: self.change_button('left'))
                self.Left_button_2.grid(row = 0, column = 0, padx = (0, 120))

                self.end_button = ctk.CTkButton(self.choose_buttons_frame_2, text= "END VIDEO TAKING", height = 60, width = 270, 
                                          font= ctk.CTkFont(size = 18, family = "raleway", weight= "bold"),
                                          cursor = "hand2", command= lambda: self.after(20, lambda: self.master.change_frame(self, Process_Table)))
                self.end_button.grid(row = 0, column = 1, padx = (120, 0))

            elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:

                self.choose_buttons_frame_2 = ctk.CTkFrame(self.main_frame, corner_radius = 0, fg_color = "transparent" )
                self.choose_buttons_frame_2.grid(row=2, column= 1)
                #self.right_focus_sensor()

                #choose side button
                self.right_button_2 = ctk.CTkButton(self.choose_buttons_frame_2, text= "START RIGHT LEG", height = 60, width = 270, 
                                          font= ctk.CTkFont(size = 18, family = "raleway", weight= "bold"),
                                          cursor = "hand2", command= lambda: self.change_button('left'))
                self.right_button_2.grid(row = 0, column = 0, padx = (0, 120))

                self.end_button = ctk.CTkButton(self.choose_buttons_frame_2, text= "END VIDEO TAKING", height = 60, width = 270, 
                                          font= ctk.CTkFont(size = 18, family = "raleway", weight= "bold"),
                                          cursor = "hand2", command= lambda: self.after(20, lambda: self.master.change_frame(self, Process_Table)))
                self.end_button.grid(row = 0, column = 1, padx = (120, 0))
            
            elif self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 1:
                self.after(20, lambda: self.master.change_frame(self, Process_Table))

    def toggle_recording(self, state):
        try:
            if not self.recording:
                self.recording = True
                self.record_label.configure(text="Press Stop to Start Recording")
                
                
                #self.client.connect('127.0.0.1',1883) # connect to mqtt
                #print("connecting to mqtt")
                # start a new thread
                #self.client.loop_start()
                
                #TODO: update frame numbers here
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                output_filename = f'Data_process/{self.assessment_state_text}_vid.avi'
                self.out = cv2.VideoWriter(output_filename, fourcc, 10, (1280, 720))  # Reduced frame size
                print(output_filename) 

            else:
               
                #self.client.disconnect() #disconnect
                #self.client.loop_stop()
                self.recording = False
                self.record_label.configure(text="Press Space to Start Recording")
                self.record_frame.grid_forget()

                # Frame Number go back to 0
                self.frame_number = 0
                self.change_button('choose_other')

        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")
            # Release resources if an error occurs
            if self.out is not None:
                self.out.release()
                self.out = None

    def receive_insole(self, espdata, frame_number):
        
        if self.recording:
            if self.assessment_state == 'left':
                self.master.frame_numbers_insole['Left'][frame_number] = espdata
                print(f"Left: {self.frame_number} : {espdata}")
                
            else:
                self.master.frame_numbers_insole['Right'][frame_number] = espdata
                print(f"Right: {self.frame_number} : {espdata}")

    def camera_update_thread(self):
        label = ttk.Label(self.web_cam_frame)
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
                #see current fps
                #self.nft = time.time()
                #self.fps = 1/(self.nft-self.pft)
                #self.pft = self.nft
                #self.fps = int(self.fps)
                #print(self.fps)
                #see current fps end
                self.web_cam_frame.update_idletasks()
                self.web_cam_frame.update()
            
            # Schedule the next frame update
            self.web_cam_frame.after(33, update_frame)  # 33 milliseconds ~= 30 fps

        # Start the initial frame update
        update_frame()

    def destroy(self):
        self.cap.release()  
        super().destroy()

#Patient's Records
class patient_Records(MenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        #create a frame for the patient records
        self.patient_records_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color= "transparent")
        self.patient_records_frame.grid(row = 0, column = 1, pady = 80, padx = 80, sticky = "nsew")
        self.record_button.configure(fg_color=("gray75", "gray25"))

        #configure the grid for the patient record
        self.patient_records_frame.grid_rowconfigure(2, weight= 1)
        self.patient_records_frame.grid_columnconfigure(0, weight=1)

        #Title frame
        self.title_frame = ctk.CTkFrame(self.patient_records_frame, corner_radius= 0, fg_color= "transparent")
        self.title_frame.grid(row = 0, column=0)

        self.title_label = ctk.CTkLabel(self.title_frame, text= "Patient's Records", font= ctk.CTkFont(size = 32, weight = "bold", family="Raleway"))
        self.title_label.grid(row = 0, column = 0, pady = (30, 20))

        #search bar frame
        self.search_bar_frame = ctk.CTkFrame(self.patient_records_frame, corner_radius= 0)
        self.search_bar_frame.grid(row = 1 , column = 0, sticky="w")

        #search bar ctkEntry
        self.search_input = ctk.CTkEntry(self.search_bar_frame, placeholder_text= "Enter the Patient ID", width = 500, height = 40,
                                         font = ctk.CTkFont(size = 16, family= "montserrat"))
        self.search_input.pack(side = tk.LEFT, padx = 10, pady = 50)

        #search bar icon
        self.search_bar_icon = ctk.CTkButton(self.search_bar_frame, text="", image= self.master.search_icon, height = 40, width = 80, cursor = "hand2")
        self.search_bar_icon.pack(side = tk.LEFT, padx = 10, pady = 50)
    
        #scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self.patient_records_frame, corner_radius= 0)
        self.scrollable_frame.grid(row=2, column=0, sticky= "nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight= 1)

        for i in range(5):
            self.box_frame = ctk.CTkFrame(self.scrollable_frame, corner_radius= 10, fg_color= "#1F6AA5", height = 120)
            self.box_frame.grid(row = i, column = 0, padx= 20, pady= 10, sticky = "ew")
            self.box_frame.grid_columnconfigure(1, weight= 1)

            #title of the assessment
            self.assessment_title = ctk.CTkLabel(self.box_frame, text= f"Assessment_sample {i}", font= ctk.CTkFont(size= 20, family= "montserrat", weight = "bold"))
            self.assessment_title.grid(row = 0, column = 0, padx = 30, pady = 35)

            #buttons view and delete
            self.buttons_frame = ctk.CTkFrame(self.box_frame, corner_radius= 0, fg_color= "transparent") 
            self.buttons_frame.grid(row = 0, column = 2, padx = 10, pady = 0)

            self.view_button = ctk.CTkButton(self.buttons_frame, text="", image= self.master.eye_icon, height = 40, width = 80, cursor = "hand2",
                                            command = lambda:self.master.open_popupWindow(popupWindow_Table))
            self.view_button.pack(side = tk.LEFT, padx = 10)
            self.delete_button = ctk.CTkButton(self.buttons_frame, text="", image= self.master.delete_icon, height = 40, width = 80, cursor = "hand2")
            self.delete_button.pack(side = tk.LEFT, padx = 10)

class popupWindow_Table(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        size = [1440, 900]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title('Assessment Table')

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        #create a frame for the table 
        self.patientTable_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color= "transparent")
        self.patientTable_frame.grid(row = 0, column = 0, pady = 60, padx = 60, sticky = "nsew")

        #configure the grid for the table 
        self.patientTable_frame.grid_rowconfigure(2, weight= 1)
        self.patientTable_frame.grid_columnconfigure(0, weight=1)

        self.tableTitle = ctk.CTkLabel(self.patientTable_frame, text= "Sample Table for Assessment", font= ctk.CTkFont(size = 32, weight = "bold", family="Raleway"))
        self.tableTitle.grid(row = 0, column = 0, pady = (40, 0))

        #tool frames
        self.tool_frame = ctk.CTkFrame(self.patientTable_frame, corner_radius= 0, fg_color= "transparent")
        self.tool_frame.grid(row = 1 , column = 0, sticky="ew", pady = (80, 40))

        #leg option menu
        self.leg_scroll = ctk.CTkOptionMenu(self.tool_frame, values=["Right Leg", "Left Leg"], 
                                                    font = ctk.CTkFont(size=16, family= "montserrat"), 
                                                    width = 250, height = 40, command ="")
        self.leg_scroll.pack(side=tk.LEFT, padx = 30)

        #gait phase
        self.leg_phase_label = ctk.CTkLabel(self.tool_frame, font = ctk.CTkFont(size=18, family= "montserrat", weight= "bold"), text= "Gait Phase:")
        self.leg_phase_label.pack(side=tk.LEFT, padx = 20)
        self.leg_phase_scroll = ctk.CTkOptionMenu(self.tool_frame, values=["1", "2", "3", "4", "5", "6", "7", "8" ], 
                                                    font = ctk.CTkFont(size=16, family= "montserrat"), 
                                                    width = 200, height = 40, command ="")
        self.leg_phase_scroll.pack(side=tk.LEFT, padx = 20)

        #search button
        self.search_button = ctk.CTkButton(self.tool_frame, text="", image= self.master.search_icon, width = 80, command= "")
        self.search_button.pack(side = tk.LEFT, padx = 20)

        #refresh button frame
        self.refresh_button_frame = ctk.CTkFrame(self.patientTable_frame, corner_radius= 0, fg_color= "transparent")
        self.refresh_button_frame.grid(row = 1 , column = 0, sticky="e", pady = (80, 40))

        #refresh button
        self.refresh_button = ctk.CTkButton(self.refresh_button_frame, width = 100, text= "SUBMIT", height = 40, cursor = "hand2",
                                            font = ctk.CTkFont(size = 16, weight= "bold", family= "raleway"))
        self.refresh_button.pack(side = tk.RIGHT, padx = 20)

class regPatient(MenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        #create a frame for the register patient
        self.reg_patient_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color= "transparent")
        self.reg_patient_frame.grid(row = 0, column = 1, pady = 80, padx = 80, sticky = "nsew")
        self.register_patient_button.configure(fg_color=("gray75", "gray25"))

        #configure the grid for the register patient frame
        self.reg_patient_frame.grid_rowconfigure(2, weight= 2)
        self.reg_patient_frame.grid_columnconfigure(0, weight=1)

        #Title frame
        self.title_frame = ctk.CTkFrame(self.reg_patient_frame, corner_radius= 0, fg_color= "transparent")
        self.title_frame.grid(row = 0, column=0)

        self.title_label = ctk.CTkLabel(self.title_frame, text= "Register Patient", font= ctk.CTkFont(size = 32, weight = "bold", family="Raleway"))
        self.title_label.grid(row = 0, column = 0, pady = (30, 20))

        #search bar frame
        self.search_bar_frame = ctk.CTkFrame(self.reg_patient_frame, corner_radius= 0)
        self.search_bar_frame.grid(row = 1 , column = 0, sticky="w")

        #search bar ctkEntry
        self.search_input = ctk.CTkEntry(self.search_bar_frame, placeholder_text= "Enter the Patient ID", width = 500, height = 40,
                                         font = ctk.CTkFont(size = 16, family= "montserrat"))
        self.search_input.pack(side = tk.LEFT, padx = 10, pady = 50)

        #search bar icon
        self.search_bar_icon = ctk.CTkButton(self.search_bar_frame, text="", image= self.master.search_icon, height = 40, width = 80, cursor = "hand2")
        self.search_bar_icon.pack(side = tk.LEFT, padx = 10, pady = 50)

        #register button frame
        self.add_button_frame = ctk.CTkFrame(self.reg_patient_frame, corner_radius= 0, fg_color= "transparent")
        self.add_button_frame.grid(row = 1 , column = 0, sticky="e", pady = (40, 40))

        #modify
        self.modify_button = ctk.CTkButton(self.add_button_frame, width = 100, text= "MODIFY", height = 40, cursor = "hand2",
                                            font = ctk.CTkFont(size = 16, weight= "bold", family= "raleway"), 
                                            command = lambda:self.master.open_popupWindow_reg(popupWindow_register,"Modify"))
        self.modify_button.pack(side = tk.RIGHT, padx = (20, 10))

        #Add button
        self.add_button = ctk.CTkButton(self.add_button_frame, width = 100, text= "ADD PATIENT", height = 40, cursor = "hand2",
                                            font = ctk.CTkFont(size = 16, weight= "bold", family= "raleway"), 
                                            command = lambda:self.master.open_popupWindow_reg(popupWindow_register, "Register"))
        self.add_button.pack(side = tk.RIGHT, padx = (10, 20))

        #Table Widget
        self.table_register_patient = ttk.Treeview(self.reg_patient_frame, columns = ('FName', 'LName', 'Age', 'Gender', 'Address', 'Birthdate', 'Tools'), show= 'headings')
        self.table_register_patient.heading('FName', text = "First Name")
        self.table_register_patient.heading('LName', text = "Last Name")
        self.table_register_patient.heading('Age', text = "Age")
        self.table_register_patient.heading('Gender', text = "Gender")
        self.table_register_patient.heading('Address', text = "Adddress")
        self.table_register_patient.heading('Birthdate', text = "Birthdate")
        self.table_register_patient.heading('Tools', text = "Tools")
        self.table_register_patient.grid(row = 2, column= 0, sticky = "nsew")

        
class popupWindow_register(ctk.CTkToplevel):
    def __init__(self, parent, string):
        super().__init__(parent)

        size = [450, 720]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title(f'{string} Patient')

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        #create a frame for the info input
        self.info_frame = ctk.CTkFrame(self, corner_radius=0, fg_color= "transparent")
        self.info_frame.grid(row= 0, column = 0, padx = 20, pady = 20)

        self.title_label = ctk.CTkLabel(self.info_frame, text = f'{string} Patient', font = ctk.CTkFont(size = 24, weight = "bold", family = "Raleway"))
        self.title_label.grid(row = 0, column = 0, pady = (40, 20), padx = 20) 

        #create a ctkentry for patient info
        self.patient_Fname = ctk.CTkEntry(self.info_frame, width = 270, height= 40, placeholder_text= "First Name",
                                          font = ctk.CTkFont(size = 16, family = "montserrat"))
        self.patient_Fname.grid(row= 1, column = 0, padx = 20, pady = 20)

        self.patient_Lname = ctk.CTkEntry(self.info_frame, width = 270, height= 40, placeholder_text= "Last Name", 
                                          font = ctk.CTkFont(size = 16, family = "montserrat"))
        self.patient_Lname.grid(row= 2, column = 0, padx = 20, pady = 20)

        self.patient_age = ctk.CTkEntry(self.info_frame, width = 270, height= 40, placeholder_text= "Age", 
                                          font = ctk.CTkFont(size = 16, family = "montserrat"))
        self.patient_age.grid(row= 3, column = 0, padx = 20, pady = 20)

        self.patient_address= ctk.CTkEntry(self.info_frame, width = 270, height= 40, placeholder_text= "Address", 
                                          font = ctk.CTkFont(size = 16, family = "montserrat"))
        self.patient_address.grid(row= 4, column = 0, padx = 20, pady = 20)

        #gender option menu
        self.patient_gender = ctk.CTkOptionMenu(self.info_frame, values=["Male", "Female"], 
                                                    font = ctk.CTkFont(size=16, family= "montserrat"), 
                                                    width = 270, height = 40, command ="")
        self.patient_gender.grid(row = 5, column = 0, padx = 20, pady = 20)

        #birthdate frame
        self.birthdate_frame = ctk.CTkFrame(self.info_frame, corner_radius= 0, fg_color= "transparent")
        self.birthdate_frame.grid(row = 6, column = 0, padx = 20, pady = 20)

        #birthdate
        self.patient_birthdate = ctk.CTkEntry(self.birthdate_frame, width= 210, height = 45, placeholder_text= "Birthdate",
                                                    font = ctk.CTkFont(size = 16, family = "montserrat"))
        self.patient_birthdate.grid(row = 0, column= 0, padx = 10)

        #birthdate button
        self.calendar_button = ctk.CTkButton(self.birthdate_frame, width = 40, height= 40, image= self.master.calendar_icon, text= "", cursor ="hand2", command = self.popup_calendar, 
                                             font = ctk.CTkFont(size = 18, family = "montserrat"))
        self.calendar_button.grid(row = 0,  column= 1, padx = 10)

        self.submit_button = ctk.CTkButton(self.info_frame, width = 270, height = 35, text= "Submit", cursor = "hand2", 
                                           font = ctk.CTkFont(size = 18, family = "montserrat"))
        self.submit_button.grid(row = 7, column = 0, pady = 40)

        self.popup_window_calendar = None
    
    def popup_calendar(self):
        if self.popup_window_calendar is None or not self.popup_window_calendar.winfo_exists():
            self.popup_window_calendar = calendarWindow(self)
            self.popup_window_calendar.attributes('-topmost', 'true') 
        else:
            self.popup_window_calendar.focus()

    def send_date(self, selected_date):
        self.patient_birthdate.delete(0, "end")
        self.patient_birthdate.insert(0, selected_date)

class calendarWindow(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.title("Calendar Picker")

        self.selected_date = None

        self.calendar = Calendar(self, font="Arial 14", selectmode='day', locale='en_US',
                   cursor="hand2", year=2024, month=4, day=19)

        self.calendar.pack(fill="both", expand=True)

        self.calendar.bind("<<CalendarSelected>>", self.update_selected_date)

        self.calendar_submit = ctk.CTkButton(self.calendar, text = "submit", bg_color= "gray", font = ctk.CTkFont(size = 18, family= "raleway", weight="bold"),
                                             corner_radius= 0, height = 35, command = lambda:self.master.send_date(self.selected_date))
        self.calendar_submit.pack(fill="both", expand=True)
    
    def update_selected_date(self, event):
        self.selected_date = self.calendar.selection_get()

class Account_Settings(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        size = [600, 400]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        #Main Info Frame
        self.account_settings_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color="transparent") 
        self.account_settings_frame.grid(row = 0, column= 0, padx = 20, pady = 20)

        self.pin_Number = ctk.CTkLabel(self.account_settings_frame, text= "Change Pin Number", font= ctk.CTkFont(size= 22, family= "raleway", weight= "bold"))
        self.pin_Number.grid(row = 0, column = 0, pady= (20, 40))

        self.pin_Number_orig = ctk.CTkEntry(self.account_settings_frame, height = 40, width = 270, placeholder_text= "Enter the Old Pin Number", 
                                             font= ctk.CTkFont(size = 16, family = "montserrat"))
        self.pin_Number_orig.grid(row = 1, column= 0, padx = 20, pady = 20)

        self.pin_Number_new = ctk.CTkEntry(self.account_settings_frame, height = 40, width = 270, placeholder_text= "Enter the New Pin Number", 
                                           font= ctk.CTkFont(size = 16, family = "montserrat"))
        self.pin_Number_new.grid(row = 2, column= 0, padx = 20, pady = 20)

        #Button Frames
        self.button_frame = ctk.CTkFrame(self.account_settings_frame, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row = 3, column = 0, pady=(40, 20)) 
        self.proceed_button = ctk.CTkButton(self.button_frame, height= 40, width = 200, text= "CHANGE PASSWORD", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = "")
        self.proceed_button.pack(side = tk.LEFT, padx = 10)
        self.change_button = ctk.CTkButton(self.button_frame, height= 40, width = 200, text= "CANCEL", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = self.close)
        self.change_button.pack(side = tk.LEFT, padx = 10)
    
    def close(self):
        self.destroy()
        
if __name__ == "__main__":
    app = refApp((1920, 1080))
    app.state('normal')
    app.mainloop()