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
        
        # Calculate the x and y coordinates for the window to be centered
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title("Gait Insight Device")
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title_frame = title(self)
        self.title_frame.pack(fill="both", expand=True)
        
class title(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.bg_image_label = ctk.CTkLabel(self, image=self.master.bg_image, text="")
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color= "transparent", bg_color = "transparent")
        self.main_frame.grid(row=0, column=0)
        
        #Login Frame
        self.login_frame = ctk.CTkFrame(self.main_frame, corner_radius = 0, fg_color= "white")
        
        #Menu Frame
        self.menuFrame =ctk.CTkFrame(self, corner_radius= 0, fg_color= "white")
        
        
        #create a logo
        self.logo_image_label = ctk.CTkLabel(self.login_frame, image= self.master.logo_image, text="")
        self.logo_image_label.grid(row=0, column=0, padx=80, pady=(80, 15))
        self.login_label = ctk.CTkLabel(self.login_frame, text="Login to your Accountss", font= ctk.CTkFont(family= "Raleway", size=24, weight="bold"), text_color= "#03045e")
        self.login_label.grid(row=1, column=0, padx=80, pady=(15, 15))
        self.pin_entry = ctk.CTkEntry(self.login_frame, width=270, height= 45, placeholder_text="Pin Number", fg_color= "#d3d3d3", text_color= "black", placeholder_text_color= "black", border_color= "#FAFAFA")
        self.pin_entry.grid(row=3, column=0, padx= 80, pady=(5, 20))
        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.mainMenu, width=270, font= ctk.CTkFont(size= 14, weight= "bold"), height = 35)
        self.login_button.grid(row=4, column=0, padx=80, pady=(10, 80))
        
        self.login_frame.grid(row=0, column=0)
        
    def mainMenu(self):
        self.login_frame.grid_forget()
        
        #create a title and logo
        self.logo_label = ctk.CTkLabel(self.menuFrame, image= "", text="")
        self.title_label = ctk.CTkLabel(self.menuFrame, font= ctk.CTkFont(family= "Raleway", size = 28, weight= "bold"), text= "Navigation Menu" , text_color= "#03045e")
        self.logo_label.grid(row = 0, column = 0, padx = 80, pady = (80, 15))
        self.title_label.grid(row = 1, column = 0, padx = 80, pady=(15, 15))
        
        #assessment button
        self.assessment_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image ="", text= "Start Assessment", 
                                               font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2",
                                                command=lambda: self.master.change_frame(self, StartAssessment))
        self.assessment_button.grid(row = 2, column = 0, padx = 80, pady = (25, 15))
 
        #records button
        self.records_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image = "", text= "Patient Records", 
                                            font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2", 
                                            command=lambda: self.master.change_frame(self, patient_Records))
        self.records_button.grid(row = 3, column = 0, padx = 80, pady = (15, 15))

        #register patient button
        self.register_patient_button = ctk.CTkButton(self.menuFrame, width = 300, height= 60, image = "", text= "Register Patient", 
                                                     font =ctk.CTkFont(family= "Raleway", size=18, weight= "bold"), cursor= "hand2", 
                                                     command=lambda: self.master.change_frame(self, regPatient))
        self.register_patient_button.grid(row = 5, column = 0, padx = 80, pady = (15, 80))
        
        self.menuFrame.grid(row=0, column=0)
        
        
if __name__ == "__main__":
    app = refApp((1920, 1080))
    app.state('normal')
    app.mainloop()
