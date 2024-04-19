import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage
from PIL import Image, ImageTk
import cv2
#import mediapipe as mp
import os
#import numpy as np
import math 
#from tensorflow.keras.models import load_model
import threading
import customtkinter as ctk
from tkcalendar import Calendar, DateEntry

class refApp(ctk.CTk):
    def __init__(self, size):

        # main setup
        super().__init__()
        self.title('Gait Insight Device')

        # Calculate the x and y coordinates for the window to be centered
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title("Gait Insight Device")
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.iconbitmap(current_path +"/img/trial logo.ico")

        #side_flag
        self.side_flag = 'None'
        self.current_patient = 'None'

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title_frame = title(self, size)
        self.title_frame.pack(fill="both", expand=True)
    
    def change_frame(self, current_frame, next_frame_class):
        #current frame change removed
        current_frame.pack_forget()

        #new frame will show
        self.next_frame_class = next_frame_class
        self.current_frame = self.next_frame_class(self)
        self.current_frame.pack(fill='both', expand=True)
        
        if isinstance(current_frame, Side_Cam):
            current_frame.destroy()

class title(ctk.CTkFrame):
    def __init__(self, parent, size):
        super().__init__(parent)

        # image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.logo_image = ctk.CTkImage(Image.open(current_path + "/img/trial logo 2.png"),size= (236, 376))
        
        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = ctk.CTkImage(Image.open(current_path + "/img/bg_gradient.jpg"),size= (size[0], size[1]))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = ctk.CTkFrame(self, corner_radius=0, width= 520, height= 720, fg_color= "white")
        self.login_frame.grid(row=0, column=0)
        
        #create a logo
        self.logo_image_label = ctk.CTkLabel(self.login_frame, image= self.logo_image, text="")
        self.logo_image_label.grid(row=0, column=0, padx=80, pady=(80, 15))
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login to your Account", font= ctk.CTkFont(family= "Raleway", size=24, weight="bold"), text_color= "#03045e")
        self.login_label.grid(row=1, column=0, padx=80, pady=(15, 15))
        self.username_entry = ctk.CTkEntry(self.login_frame, width=270, height= 45, placeholder_text="Username", fg_color= "#d3d3d3", text_color= "black", placeholder_text_color= "black", border_color= "#FAFAFA")
        self.username_entry.grid(row=2, column=0, padx= 80, pady=(20, 20))
        self.username_entry = ctk.CTkEntry(self.login_frame, width=270, height= 45, placeholder_text="Password", fg_color= "#d3d3d3", text_color= "black", placeholder_text_color= "black", border_color= "#FAFAFA")
        self.username_entry.grid(row=3, column=0, padx= 80, pady=(5, 20))
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=lambda: self.master.change_frame(self, MainMenu), width=270, font= ctk.CTkFont(size= 14, weight= "bold"), height = 35)
        self.login_button.grid(row=4, column=0, padx=80, pady=(10, 80))

class MainMenu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.bg_image = ctk.CTkImage(Image.open(current_path + "/img/bg_gradient.jpg"),size= (1920, 1080))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # load logo Image 
        self.logo_image = ctk.CTkImage(Image.open(current_path + "/img/trial logo.png"),size= (200, 200))

        #create a Menu Frame
        self.menuFrame =ctk.CTkFrame(self, corner_radius= 0, fg_color= "white")
        self.menuFrame.grid(row=0, column=0)

        #create a title and logo
        self.logo_label = ctk.CTkLabel(self.menuFrame, image= self.logo_image, text="")
        self.title_label = ctk.CTkLabel(self.menuFrame, font= ctk.CTkFont(family= "Raleway", size = 28, weight= "bold"), text= "Navigation Menu" , text_color= "#03045e")
        self.logo_label.grid(row = 0, column = 0, padx = 80, pady = (80, 15))
        self.title_label.grid(row = 1, column = 0, padx = 80, pady=(15, 15))
        
        #open icons 
        self.assessment_icon = ctk.CTkImage(Image.open(current_path+"/img/assessment.png"), size = (40, 40))
        self.records_icon = ctk.CTkImage(Image.open(current_path+"/img/verify.png"), size = (40, 40))
        self.register_user_icon = ctk.CTkImage(Image.open(current_path+"/img/users.png"), size = (40, 40))
        self.register_patient_icon = ctk.CTkImage(Image.open(current_path+"/img/patient.png"), size =(40, 40))

        #assessment button
        self.assessment_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image =self.assessment_icon, text= "Start Assessment", 
                                               font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2",
                                                command=lambda: self.master.change_frame(self, StartAssessment))
        self.assessment_button.grid(row = 2, column = 0, padx = 80, pady = (25, 15))
 
        #records button
        self.records_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image =self.records_icon, text= "Patient Records", 
                                            font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2", 
                                            command=lambda: self.master.change_frame(self, patient_Records))
        self.records_button.grid(row = 3, column = 0, padx = 80, pady = (15, 15))

        #register patient button
        self.register_patient_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image =self.register_patient_icon, text= "Register Patient", 
                                                     font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2", 
                                                     command=lambda: self.master.change_frame(self, regPatient))
        self.register_patient_button.grid(row = 5, column = 0, padx = 80, pady = (15, 80))

        #register button
        self.register_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image =self.register_user_icon, text= "Account Settings", 
                                             font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2")
        self.register_button.grid(row = 4, column = 0, padx = 80, pady = (15, 15))
        

class MenuBar(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #load images icon for navigation pane
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.logo_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "trial logo.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "trial logo-light.png")), size=(80, 80))

        #Navigation Bar Icons
        self.assessment_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "assessment.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "assessment-light.png")), size=(40, 40))
        self.records_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "verify.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "verify-light.png")), size=(40, 40))
        self.register_users_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "users.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "users-light.png")), size=(40, 40))
        self.register_patient_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "patient.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "patient-light.png")), size=(40, 40))
        

        #create Navigation Frame Icons
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)


        #Title
        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text= "Gait Insight", image=self.logo_image, 
                                                             compound="left", font= ctk.CTkFont(size= 24, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx = 40, pady = 20)

        #start assessment button
        self.assessment_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Start Assessment",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.assessment_icon, anchor="center", command=lambda: self.master.change_frame(self, StartAssessment))
        self.assessment_button.grid(row=1, column=0, sticky="ew", pady=(10, 10))

        #record button
        self.record_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Patient Records",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.records_icon, anchor="center", command=lambda: self.master.change_frame(self, patient_Records))
        self.record_button.grid(row=2, column=0, sticky="ew", pady=(10, 10))
        
        #register patient button
        self.register_patient_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Register Patients",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.register_patient_icon, anchor="center", command=lambda: self.master.change_frame(self, regPatient))
        self.register_patient_button.grid(row=4, column=0, sticky="ew", pady=(10, 10))

        #Account Settings
        self.register_users_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Account Settings",
                                                   font = ctk.CTkFont(size= 16, family= "montserrat", weight= "bold"),
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.register_users_icon, anchor="center")
        self.register_users_button.grid(row=3, column=0, sticky="ew", pady=(10, 10))

        #customize appearance mode
        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"], 
                                                    font = ctk.CTkFont(size=14, family= "montserrat", weight= "bold"), 
                                                    width = 200, height = 35, command =self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=40, sticky="s")

    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

class StartAssessment(MenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        #create a frame for the start Assessment
        self.start_assessment_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color= "transparent")
        self.start_assessment_frame.grid(row = 0, column = 1, pady = 50, padx = 50)
        self.assessment_button.configure(fg_color=("gray75", "gray25"))
        
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
                                            command = self.open_popupWindow)
        self.patient_button.pack(side = tk.LEFT, padx = 10, pady= 70)
        
        self.popup_window = None

    def open_popupWindow(self):
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = popupWindow(self)
            self.popup_window.attributes('-topmost', 'true') 
        else:
            self.popup_window.focus()


class popupWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        size = [600, 400]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        #icons
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.patient_ID_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "patient-id.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "patient-id-light.png")), size=(50, 50))
        self.patient_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "patient.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "patient-light.png")), size=(50, 50))

        #Main Info Frame (title, buttons, name and ID)
        self.info_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color="transparent") 
        self.info_frame.grid(row = 0, column= 0, padx = 20, pady = 20)

        #title
        self.info_label = ctk.CTkLabel(self.info_frame, text= "Patient's Information", font= ctk.CTkFont(size= 22, family= "raleway", weight= "bold"))
        self.info_label.grid(row = 0, column = 0, pady= (20, 40))

        #Patient Info Frame
        self.patientNum_frame = ctk.CTkFrame(self.info_frame, corner_radius= 0, fg_color= "transparent")
        self.patientNum_frame.grid(row = 1, column = 0)
        
        self.ID_icon = ctk.CTkLabel(self.patientNum_frame, text="", image= self.patient_ID_icon)
        self.ID_icon.pack(side=tk.LEFT, padx = 10, pady = 20)
        
        self.patient_number = ctk.CTkLabel(self.patientNum_frame, text= "Patient's ID: ", font= ctk.CTkFont(size = 18, family= "montserrat"))
        self.patient_number.pack(side=tk.LEFT, padx = 10, pady = 20)
        self.patient_number_input = ctk.CTkLabel(self.patientNum_frame, text= "20-050146", width= 170, height = 35, font=ctk.CTkFont(size = 18, family= "montserrat", weight= "bold"))
        self.patient_number_input.pack(side=tk.LEFT, padx = 10, pady = 20)

        #Patient Name Info Frame
        self.patientName_frame = ctk.CTkFrame(self.info_frame, corner_radius= 0, fg_color= "transparent")
        self.patientName_frame.grid(row = 2, column = 0)
        self.patient_icon = ctk.CTkLabel(self.patientName_frame, text="", image= self.patient_icon)
        self.patient_icon.pack(side=tk.LEFT, padx = 10, pady = 20)
        self.patient_name = ctk.CTkLabel(self.patientName_frame, text= "Patient's Name: ", font= ctk.CTkFont(size = 18, family= "montserrat"))
        self.patient_name.pack(side=tk.LEFT, padx = 10, pady = 20)
        self.patient_name_input = ctk.CTkLabel(self.patientName_frame, text= "Selwyne Christian Ponce", width= 170, height = 35, font=ctk.CTkFont(size = 18, family= "montserrat", weight= "bold"))
        self.patient_name_input.pack(side=tk.LEFT, padx = 10, pady = 20)

        #Button Frames
        self.button_frame = ctk.CTkFrame(self.info_frame, corner_radius=0, fg_color="transparent")
        self.button_frame.grid(row = 3, column = 0, pady=(40, 20)) 
        self.proceed_button = ctk.CTkButton(self.button_frame, height= 40, width = 200, text= "PROCEED", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = lambda: self.master.change_frame(self, Side_Cam))
        self.proceed_button.pack(side = tk.LEFT, padx = 10)
        self.change_button = ctk.CTkButton(self.button_frame, height= 40, width = 200, text= "CHANGE", 
                                            font= ctk.CTkFont(size = 18, family= "Raleway", weight = "bold"), cursor= "hand2",
                                            command = self.go_back_to_assessment)
        self.change_button.pack(side = tk.LEFT, padx = 10)

    def go_back_to_assessment(self):
        self.destroy()
        self.master.focus()

#To be continued
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




#Patient's Records
class patient_Records(MenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        #icons
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.search_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "search.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "search-light.png")), size=(30, 30))
        self.delete_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "delete.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "delete-light.png")), size=(30, 30))
        self.eye_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "eye.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "eye-light.png")), size=(30, 30)) 

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
        self.search_bar_icon = ctk.CTkButton(self.search_bar_frame, text="", image= self.search_icon, height = 40, width = 80, cursor = "hand2")
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

            self.view_button = ctk.CTkButton(self.buttons_frame, text="", image= self.eye_icon, height = 40, width = 80, cursor = "hand2",
                                             command= self.open_popupWindow_table)
            self.view_button.pack(side = tk.LEFT, padx = 10)
            self.delete_button = ctk.CTkButton(self.buttons_frame, text="", image= self.delete_icon, height = 40, width = 80, cursor = "hand2")
            self.delete_button.pack(side = tk.LEFT, padx = 10)

            self.popup_window_table = None

    def open_popupWindow_table(self):
        if self.popup_window_table is None or not self.popup_window_table.winfo_exists():
            self.popup_window_table = popupWindow_Table(self)
            self.popup_window_table.attributes('-topmost', 'true') 
        else:
            self.popup_window_table.focus()

#popupWindow for Table
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

        #icons
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
        self.search_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "search.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "search-light.png")), size=(30, 30))

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
        self.search_button = ctk.CTkButton(self.tool_frame, text="", image= self.search_icon, width = 80, command= "")
        self.search_button.pack(side = tk.LEFT, padx = 20)

        #refresh button frame
        self.refresh_button_frame = ctk.CTkFrame(self.patientTable_frame, corner_radius= 0, fg_color= "transparent")
        self.refresh_button_frame.grid(row = 1 , column = 0, sticky="e", pady = (80, 40))

        #refresh button
        self.refresh_button = ctk.CTkButton(self.refresh_button_frame, width = 100, text= "REFRESH", height = 40, cursor = "hand2",
                                            font = ctk.CTkFont(size = 16, weight= "bold", family= "raleway"))
        self.refresh_button.pack(side = tk.RIGHT, padx = 20)

        #tablewidget

class regPatient(MenuBar):
    def __init__(self, parent):
        super().__init__(parent)

        #create a frame for the register patient
        self.reg_patient_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color= "transparent")
        self.reg_patient_frame.grid(row = 0, column = 1, pady = 80, padx = 80, sticky = "nsew")
        self.register_patient_button.configure(fg_color=("gray75", "gray25"))

        #configure the grid for the register patient frame
        self.reg_patient_frame.grid_rowconfigure(2, weight= 1)
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
        self.search_bar_icon = ctk.CTkButton(self.search_bar_frame, text="", image= "", height = 40, width = 80, cursor = "hand2")
        self.search_bar_icon.pack(side = tk.LEFT, padx = 10, pady = 50)

        #register button frame
        self.add_button_frame = ctk.CTkFrame(self.reg_patient_frame, corner_radius= 0, fg_color= "transparent")
        self.add_button_frame.grid(row = 1 , column = 0, sticky="e", pady = (40, 40))

        #modify
        self.modify_button = ctk.CTkButton(self.add_button_frame, width = 100, text= "MODIFY", height = 40, cursor = "hand2",
                                            font = ctk.CTkFont(size = 16, weight= "bold", family= "raleway"), 
                                            command = lambda:self.open_popupWindow_register("modify"))
        self.modify_button.pack(side = tk.RIGHT, padx = (20, 10))

        #Add button
        self.add_button = ctk.CTkButton(self.add_button_frame, width = 100, text= "ADD PATIENT", height = 40, cursor = "hand2",
                                            font = ctk.CTkFont(size = 16, weight= "bold", family= "raleway"), 
                                            command = lambda:self.open_popupWindow_register("add"))
        self.add_button.pack(side = tk.RIGHT, padx = (10, 20))

        self.popup_window_register = None

    def open_popupWindow_register(self, string):
        if self.popup_window_register is None or not self.popup_window_register.winfo_exists():
            self.popup_window_register = popupWindow_register(self, string)
            self.popup_window_register.attributes('-topmost', 'true') 
        else:
            self.popup_window_register.focus()

class popupWindow_register(ctk.CTkToplevel):
    def __init__(self, parent, string):
        super().__init__(parent)

        size = [520, 720]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title('Register Patient')

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        #icons 

        #create a frame for the info input
        self.info_frame = ctk.CTkFrame(self, corner_radius=0, fg_color= "transparent")
        self.info_frame.grid(row= 0, column = 0, padx = 20, pady = 20)

        #create a ctkentry for patient info
        self.patient_Fname = ctk.CTkEntry(self.info_frame, width = 270, height= 35, placeholder_text= "First Name")
        self.patient_Fname.grid(row= 0, column = 0, padx = 20, pady = 20)

        self.patient_Lname = ctk.CTkEntry(self.info_frame, width = 270, height= 35, placeholder_text= "Last Name")
        self.patient_Lname.grid(row= 2, column = 0, padx = 20, pady = 20)

        self.patient_age = ctk.CTkEntry(self.info_frame, width = 270, height= 35, placeholder_text= "Age")
        self.patient_age.grid(row= 3, column = 0, padx = 20, pady = 20)

        #gender option menu
        self.patient_gender = ctk.CTkOptionMenu(self.info_frame, values=["Male", "Female"], 
                                                    font = ctk.CTkFont(size=16, family= "montserrat"), 
                                                    width = 270, height = 40, command ="")
        self.patient_gender.grid(row = 4, column = 0, padx = 20, pady = 20)

        #birthdate frame
        self.birthdate_frame = ctk.CTkFrame(self.info_frame, corner_radius= 0, fg_color= "transparent")
        self.birthdate_frame.grid(row = 5, column = 0, padx = 20, pady = 20)

        #birthdate
        self.patient_birthdate = ctk.CTkEntry(self.birthdate_frame, width= 210, height = 35, placeholder_text= "Birthdate")
        self.patient_birthdate.grid(row = 0, column= 0, padx = 10)

        #birthdate button
        self.calendar_button = ctk.CTkButton(self.birthdate_frame, width = 40, height= 35, image= "", text= "", cursor ="hand2", command = self.popup_calendar)
        self.calendar_button.grid(row = 0,  column= 1, padx = 10)

        self.submit_button = ctk.CTkButton(self.info_frame, width = 270, height = 35, text= "Submit")
        self.submit_button.grid(row = 6, column = 0, pady = 80)

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
                   cursor="hand1", year=2018, month=2, day=5)

        self.calendar.pack(fill="both", expand=True)

        self.calendar.bind("<<CalendarSelected>>", self.update_selected_date)

        self.calendar_submit = ctk.CTkButton(self.calendar, text = "submit", bg_color= "gray", font = ctk.CTkFont(size = 18, family= "raleway", weight="bold"),
                                             corner_radius= 0, height = 35, command = lambda:self.master.send_date(self.selected_date))
        self.calendar_submit.pack(fill="both", expand=True)
    
    def update_selected_date(self, event):
        self.selected_date = self.calendar.selection_get()

if __name__ == "__main__":
    app = refApp((1920, 1080))
    app.state('normal')
    app.mainloop()
