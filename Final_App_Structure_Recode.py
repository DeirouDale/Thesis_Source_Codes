import tkinter as tk
from tkinter import messagebox, PhotoImage
from tkinter import ttk, messagebox, PhotoImage
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import os
import numpy as np
import math 
from tensorflow.keras.models import load_model
import threading
import multiprocessing
from tkcalendar import Calendar, DateEntry
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import mysql.connector 
from datetime import datetime
import re
import shutil #move files
import paho.mqtt.client as mqtt
import time
from datetime import datetime, timedelta

conn = mysql.connector.connect(
    host = "localhost",
    user= "gaitrpi",
    password = "gait123",
    database="gaitdata"
)
process_event = multiprocessing.Event()
class refApp(tk.Tk):
    def __init__(self, size):
        # main setup
        super().__init__()

        self.conn = conn

        self.styles()
        self.resizable(False, False)
        
        self.title("Gait Insight Device")

        # Calculate the x and y coordinates for the window to be centered
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

        #icons----------------------------------------------------------->
        current_path = os.path.dirname(os.path.realpath(__file__))

        #bitmap Icon
        #self.iconbitmap(current_path +"/img/trial logo.ico")

        self.bg_image = ImageTk.PhotoImage(Image.open(current_path + "/img/bg_gradient.jpg").resize((1280, 720)))

        #logo with name
        self.logo_image = ImageTk.PhotoImage(Image.open(current_path + "/img/trial logo 2.png").resize((150, 240)))

        #logo w/out name
        self.logo_image_3 = ImageTk.PhotoImage(Image.open(current_path + "/img/trial logo.png").resize((60, 60)))


        self.assessment_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/assessment.png")).resize((30, 30)))
        self.records_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/verify.png")).resize((30, 30)))
        self.account_user_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/users.png")).resize((20, 20)))
        self.register_patient_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/patient.png")).resize((30, 30)))
        self.log_out_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/logout.png")).resize((20, 20)))
        self.about_us_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/info.png")).resize((20, 20)))
        self.patient_ID_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/patient-id.png")).resize((30, 30)))
        self.search_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/search-light.png")).resize((20, 20)))
        self.foot_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/templates.png")).resize((175, 175)))
        self.eye_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/eye-light.png")).resize((20, 20)))
        self.delete_icon = ImageTk.PhotoImage(Image.open(os.path.join(current_path + "/img/delete-light.png")).resize((20, 20)))
        self.mmsu_logo = ImageTk.PhotoImage(Image.open(os.path.join(current_path+ "/img/mmsu-logo.png")).resize((60,60)))
        self.cpe_logo = ImageTk.PhotoImage(Image.open(os.path.join(current_path+ "/img/cpe-logo.png")).resize((60,60)))

        #images profile
        self.dale = ImageTk.PhotoImage(Image.open(os.path.join(current_path+ "/img/panganiban.png")).resize((100,100)))  
        self.salmo = ImageTk.PhotoImage(Image.open(os.path.join(current_path+ "/img/Lanz.png")).resize((100,100)))
        self.ismael = ImageTk.PhotoImage(Image.open(os.path.join(current_path+ "/img/Ismael.png")).resize((100,100)))
        self.palacio = ImageTk.PhotoImage(Image.open(os.path.join(current_path+ "/img/palacio.png")).resize((100,100)))
        self.ponce = ImageTk.PhotoImage(Image.open(os.path.join(current_path+ "/img/ponce.png")).resize((100,100)))
        self.research_ad = ImageTk.PhotoImage(Image.open(os.path.join(current_path+ "/img/research_ad.png")).resize((100,100)))


        #end------------------------------------------------------------->

        #side_flag
        self.current_patient = 'None'
        self.current_patient_id = 'None'
        self.popup_window = None
        self.side_state = {'Right': 0, 'Left':0}
        
        self.synced_left = []
        self.synced_right = []
        # Title Frame
        self.title_frame =  Title(self, self.style)
        self.title_frame.pack(fill="both", expand=True)

    def styles(self):
        self.style = ttk.Style("litera")

        self.style.configure('main.TButton', font = ("Raleway", 12, "bold"), padding = [10, 5, 10, 5])
        self.style.configure('nav.TButton', font = ("Raleway", 14, "bold"), padding = [12, 8, 12, 8])
        self.style.configure('light.TButton', font= ("Raleway", 14, "bold"), padding = [8, 15, 8, 15])
        self.style.map('light.TButton', background=[
                        ('active', '#ECECEC')])
        self.style.configure('dark.TLabel', font= ("montserrat", 10))
        self.style.configure('search.TButton', font = ("Raleway", 10, "bold"), padding = [6, 6, 6, 6])
        self.style.configure('danger.TButton', font = ("Raleway", 12, "bold"), padding = [10, 5, 10, 5])
        self.style.configure('sample.TButton', font = ("Raleway", 12, "bold"), padding = [10, 5, 10, 5], background= 'red')
        
        self.style.configure('Treeview', font = ('Arial', 8))
        self.style.configure('Treeview.Heading', font = ('Arial', 8))
    
    def open_popupWindow(self, window):
        self.window = window
        if self.popup_window is None or not self.popup_window.winfo_exists():
            self.popup_window = self.window(self)
            self.popup_window.attributes('-topmost', 'true') 
        else:
            self.popup_window.focus()
            return

    def open_popupWindow_reg(self, popup_instance):
            self.popup_window = popup_instance(self.master, self.conn)  # Pass both parent and db_connection arguments
            self.popup_window.grab_set() 
            self.popup_window.wait_window()
    
    def open_popupWindow2(self, popup_class, client_id, assessment_num, first_name, last_name, dt):
        self.popup_window = popup_class(self.master, client_id, assessment_num, first_name, last_name, dt)
        self.popup_window.grab_set() 
        self.popup_window.wait_window()

    def change_frame(self, current_frame, next_frame_class):
        
        current_frame.pack_forget()

        #new frame will show
        self.next_frame_class = next_frame_class
        self.current_frame = self.next_frame_class(self, self.style)
        
        if isinstance(self.current_frame, MenuBar):
            self.current_frame.pack()
        else:
            self.current_frame.pack(fill='both', expand=True)    
        if isinstance(current_frame, Side_Cam):
            current_frame.destroy()

class Title(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)

        self.style = style

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.bg_image  = ttk.Label(self, image = self.master.bg_image, borderwidth= 0)
        self.bg_image.grid(row = 0, column = 0)

        #create a Main Frame
        self.main_frame = ttk.Frame(self,  bootstyle = "light")
        self.main_frame.grid(row = 0, column = 0)

        #create a login frame and Menu Frame
        self.login_frame = ttk.Frame(self.main_frame,  bootstyle = "light")
        self.menu_frame = ttk.Frame(self.main_frame,  bootstyle = "light")
        self.login_frame.grid(row = 0, column = 0)

        self.school_logo_frame = ttk.Frame(self.login_frame, bootstyle = 'light')
        self.school_logo_frame.grid(row = 0, column = 0, padx = 40, pady = 20)

        self.mmsu_logo = ttk.Label(self.school_logo_frame, image = self.master.mmsu_logo, text= "", bootstyle= "inverse-light")
        self.mmsu_logo.grid(row= 0, column = 0, padx=(0, 10))

        self.cpe_logo = ttk.Label(self.school_logo_frame, image = self.master.cpe_logo, text= "", bootstyle= "inverse-light")
        self.cpe_logo.grid(row= 0, column = 1, padx=(0, 10))

        #create a logo and elements
        self.logo_image_label = ttk.Label(self.login_frame, image= self.master.logo_image, text="", bootstyle= "inverse-light")
        self.logo_image_label.grid(row=1, column=0, padx=40, pady=(15, 15))
        self.login_label = ttk.Label(self.login_frame, text="Login to your Accounts", font= ( "Raleway", 14,"bold"), bootstyle= 'inverse-light')
        self.login_label.grid(row=2, column=0, padx=40, pady=(15, 15))
        self.pin_entry = ttk.Entry(self.login_frame, font= ('montserrat', 12, 'bold'), bootstyle = 'default', show= '*')
        self.pin_entry.grid(row = 3, column = 0, padx=40, pady=(15, 15))
        self.login_button = ttk.Button(self.login_frame, text="Login", command= self.login, 
                                       bootstyle = 'primary', cursor = 'hand2', width = 13, style= 'main.TButton', takefocus= False)
        self.login_button.grid(row=5, column=0, padx=40, pady=(10, 60))

    def login(self):
        pin = self.pin_entry.get()
        if validate_pin(pin):
            self.master.change_frame(self, MenuBar)
        else:
            messagebox.showerror("Error", "Invalid Pin")
  
def detect_esp(queue,flag): #run every 5 seconds
    global process_event
    print("Starting process")
    timer = time.time()
    while True:
        if time.time() - timer >2:
            timer = time.time()
            print("Detecting esp")        
            response1 = os.system("ping -c 1 -w 1 192.168.0.184 >/dev/null 2>&1")
            response2 = os.system("ping -c 1 -w 1 192.168.0.171 >/dev/null 2>&1")
            if response1 == 0 and response2 == 0:
                #detect
                esp_status = "Detected"
                color_esp = "success"
            else:
                #not fully detected
                esp_status = "Not Detected"
                color_esp = "danger"
                #self.insole_label.config(text= f"Status: {self.esp_status}")

            queue.put((esp_status,color_esp))
        if flag == 0 or process_event.is_set():
            print("Killing process")
            queue.put("Stop",'danger')
            break

class MenuBar(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
        
        self.conn = mysql.connector.connect(
        host = "localhost",
	    user= "gaitrpi",
	    password = "gait123",
	    database="gaitdata"
        )
        
        self.master.side_state['Right'] = 0
        self.master.side_state['Left'] = 0
        self.cursor = self.conn.cursor()
        self.client_id = None
        self.style = style
        self.start_time = time.time()
        self.esp_detect = 0
        self.esp_status = None
        self.color_esp = 'danger'
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #create Navigation Frame icons
        self.navigation_frame = ttk.Frame(self, borderwidth= 0, bootstyle = 'light')
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        #Title
        self.navigation_frame_label = ttk.Label(self.navigation_frame, text= "Gait Insight", image=self.master.logo_image_3, bootstyle = 'inverse-light',
                                                             compound="left", font= ("Raleway", 18, "bold"), takefocus= False)
        self.navigation_frame_label.grid(row=0, column=0, padx = 30, pady =20)

        #Navigation Icons
        self.assessment_button = ttk.Button(self.navigation_frame, image= self.master.assessment_icon, text= "Start Assessment", 
                                            cursor = "hand2", compound = "left", style = 'light.TButton', takefocus= False,
                                            command= self.StartAssessment)
        self.assessment_button.grid(row=1, column=0, sticky="ew", pady=(10, 5))

        #Records Icons
        self.records_button = ttk.Button(self.navigation_frame, image= self.master.records_icon, text= "Patient Records",
                                            cursor = "hand2", compound = "left", style = 'light.TButton', takefocus= False,
                                            command= self.Patients_records)
        self.records_button.grid(row=2, column=0, sticky="ew", pady=(5, 5))

        #About us
        self.about_us_button = ttk.Button(self.navigation_frame, image= self.master.about_us_icon, text= "About us",  
                                            cursor = "hand2", compound = "left", style = 'light.TButton', takefocus= False,
                                            command = self.about_us)
        self.about_us_button.grid(row=6, column=0, pady=(5, 5), sticky="ews")

        #Register Icons
        self.register_button = ttk.Button(self.navigation_frame, image= self.master.register_patient_icon, text= "Register Patients",  
                                            cursor = "hand2", compound = "left", style = 'light.TButton', takefocus= False,
                                            command= self.reg_Patients)
        self.register_button.grid(row=3, column=0, sticky="ew", pady=(5, 10))

        #Account Settings
        self.account_setting = ttk.Button(self.navigation_frame, image= self.master.account_user_icon, text= "Account Settings",  
                                            cursor = "hand2", compound = "left", style = 'light.TButton', takefocus= False,
                                            command = lambda:self.master.open_popupWindow_reg(Account_Settings))
        self.account_setting.grid(row=5, column=0, pady=(5,5), sticky="ews")

        #Log out 
        self.Log_out = ttk.Button(self.navigation_frame, image= self.master.log_out_icon, text= "Log out",  
                                            cursor = "hand2", compound = "left", style = 'light.TButton', takefocus= False,
                                            command = lambda: [self.stop_esp(),self.master.change_frame(self, Title)])
        self.Log_out.grid(row=7, column=0, pady=(5, 20), sticky="ews")

        self.main_frame = ttk.Frame(self, borderwidth=0, bootstyle = 'light')
        self.main_frame.grid(row = 0, column = 1, padx= 20, pady = 20, sticky= "nsew")

        self.main_frame.grid_columnconfigure(0, weight = 1)
        self.main_frame.grid_rowconfigure(3, weight = 1)

        self.StartAssessment()
            
    #frame 1 -----> Start Assessment of the Patients
    def StartAssessment(self):
        global process_event
        self.StartAssessment_frame = ttk.Frame(self.main_frame, borderwidth=0, bootstyle= 'light')
        self.StartAssessment_frame.grid(row = 0, column = 0, padx = 20, pady = 20, sticky= "nsew")

        self.StartAssessment_frame.grid_columnconfigure(0, weight = 1)
        self.StartAssessment_frame.grid_rowconfigure(0, weight = 1)

        self.title_label = ttk.Label(self.StartAssessment_frame, text = "Gait Assessment Section", font= ("Raleway", 18, 'bold'), bootstyle = "inverse-light")
        self.title_label.grid(row = 0, column = 0, pady=(20,10))

        #label warnings
        self.label_frame = ttk.LabelFrame(self.StartAssessment_frame, text= " Instructions ", style = 'primary')
        self.label_frame.grid(row = 1, column = 0, pady=(10,10), sticky = "ew")

        self.warning = ttk.Label(self.label_frame, text= "1. Room should be well lit and background white in color. ", style= 'dark.TLabel')
        self.warning.grid(row = 0, column = 0, padx= 20, pady=(10,5))

        self.warning_2 = ttk.Label(self.label_frame, text= "2. Client should be out of the frame before recording.       ", style= 'dark.TLabel')
        self.warning_2.grid(row = 1, column = 0, padx= 20, pady=(5,5))
        
        self.warning_3 = ttk.Label(self.label_frame, text= "3. Client head to feet should be visible on screen.                ", style= 'dark.TLabel')
        self.warning_3.grid(row = 2, column = 0, padx= 20, pady=(5,10))

        #lower frames 
        self.second_frame = ttk.Frame(self.StartAssessment_frame, borderwidth=0)
        self.second_frame.grid(row = 2, column = 0, sticky = "nsew")

        self.second_frame.grid_columnconfigure(1, weight = 1)
        self.second_frame.grid_rowconfigure(0, weight = 1)

        #insole syncing frame
        self.insole_syncing_frame = ttk.Labelframe(self.second_frame, text= "Pressure Insole Status", style = 'primary')
        self.insole_syncing_frame.grid(row= 0, column = 0, pady=(10, 10))

        self.insole_status = ttk.Label(self.insole_syncing_frame, text= "Pressure Insole Sensor", font=('Raleway', 14, 'bold'))
        self.insole_status.grid(row = 0, column = 0, padx = 20, pady=(20,30))

        self.insole = ttk.Label(self.insole_syncing_frame, image = self.master.foot_icon)
        self.insole.grid(row = 1, column = 0, padx = 20, pady=(10,10))

        self.insole_label = ttk.Label(self.insole_syncing_frame, text = f"Status:{self.esp_status}", bootstyle= f"{self.color_esp}", font=('raleway', 14, 'bold'))
        self.insole_label.grid(row = 2, column = 0, padx = 20, pady=(20,40))

        #icons patient
        self.patient_number = ttk.Labelframe(self.second_frame, text= "Patient Input", style = 'primary')
        self.patient_number.grid(row = 0, column = 1, sticky = "nsew", padx = 10, pady= 10)

        self.patient_number.grid_columnconfigure(0, weight = 1)
        self.patient_number.grid_rowconfigure(1, weight = 1)

        self.patient_label = ttk.Label(self.patient_number, text= "Select Current Patient", font=('Raleway', 14, 'bold'))
        self.patient_label.grid(row = 0, column = 0, pady=(30,20))

        self.patient_info_frame = ttk.Frame(self.patient_number, borderwidth= 0)
        self.patient_info_frame.grid(row = 1, column = 0, pady= (10,10))

        self.patient_num = ttk.Label(self.patient_info_frame, font=('Montserrat',10, 'bold'), text=f"Patient Number: {self.master.current_patient_id}")
        self.patient_num.grid(row = 0, column = 0, padx = 20, pady= (10,10))
        self.patient_name = ttk.Label(self.patient_info_frame, font=('montserrat', 10, 'bold'), text=f"Patient Name: {self.master.current_patient}")
        self.patient_name.grid(row = 1, column = 0, padx = 20, pady= (10,10))

        self.patient_entry_frame = ttk.Frame(self.patient_number, borderwidth= 0)
        self.patient_entry_frame.grid(row = 2, column = 0, pady= (10,10))

        self.patient_entry = ttk.Entry(self.patient_entry_frame, font= ('montserrat', 10, 'bold'), bootstyle = 'default', width= 25)
        self.patient_entry.grid(row = 0, column = 0, padx=10, pady=(15, 25))

        self.submit_button = ttk.Button(self.patient_entry_frame, text="submit", command= self.submit_button_get_info, 
                                       bootstyle = 'primary', cursor = 'hand2', width = 8, style= 'search.TButton', takefocus= False)
        self.submit_button.grid(row=0, column=1, padx=10, pady=(15, 25))

        self.proceed_button = ttk.Button(self.patient_number, text= "Proceed to Assessment", command= lambda: [self.stop_esp(),self.master.change_frame(self, Side_Cam)]
                                         , style= 'main.TButton', takefocus= False, cursor= 'hand2', state='disabled')
        self.proceed_button.grid(row=3, column=0, padx=10, pady=(15, 40))
        self.start_esp_detect()
        
    def start_esp_detect(self):
        #esp detection flag
        if self.esp_detect == 0:
            self.esp_detect = 1
            process_event.clear()
            self.queue = multiprocessing.Queue()
            self.esp_thread = threading.Thread(target=self.update_esp_status,daemon=True)
            if not self.esp_thread.is_alive():
                self.esp_thread.start()
    def update_esp_status(self):
        self.esp_process = multiprocessing.Process(target=detect_esp,args=(self.queue,self.esp_detect),daemon=True)
        #if process is running
        if not self.esp_process.is_alive():
            self.esp_process.start()
        timer = 0
        while True:
            esp_status, self.color_esp = self.queue.get()
            #print(self.color_esp)
            #print(esp_status)
            if esp_status != "Stop":
                self.insole_label.config(text= f"Status: {esp_status}",bootstyle= f"{self.color_esp}")
            elif self.esp_detect == 0 or esp_status == "Stop":
                print("Killing thread")
                break
        print("thread killed")
    def stop_esp(self):
        global process_event
        process_event.set()
        print("stop_esp has been called")
        self.esp_detect=0
    def pack(self):
        global process_event
        print("back to menu")
        super(MenuBar,self).pack(fill="both",expand=True)
        self.esp_detect = 0
        self.start_esp_detect()
    def submit_button_get_info(self):        
        conn = mysql.connector.connect(
        host = "localhost",
	    user= "gaitrpi",
	    password = "gait123",
	    database="gaitdata"
        )
        client_id = self.patient_entry.get()
        cursor = conn.cursor()
        cursor.execute("SELECT first_name, last_name FROM patient_info WHERE client_id = %s",(client_id,))
        
        name = cursor.fetchone()
        
        if name is not None:
            fullname = name[0]+' '+name[1]
            self.master.current_patient = fullname
            self.master.current_patient_id = client_id
            
            self.patient_num.config(text= f"Patient Number: {self.master.current_patient_id}")
            self.patient_name.config(text= f"Patient Name: {self.master.current_patient}")
            
            self.proceed_button.config(state = 'normal')
          
        else:
            messagebox.showerror("Error", "Client ID does not exist!")
            self.master.current_patient = 'None'
            self.master.current_patient_id = 'None'
            
            self.patient_num.config(text= f"Patient Number: {self.master.current_patient_id}")
            self.patient_name.config(text= f"Patient Name: {self.master.current_patient}")
            self.proceed_button.config(state = 'disabled')
            
        self.patient_entry.delete(0, 'end')
            

    #Frame 4 about us
    def about_us(self):
        self.stop_esp()
        self.about_us_frame = ttk.Frame(self.main_frame, borderwidth=0, bootstyle= 'light')
        self.about_us_frame.grid(row = 0, column = 0, padx = 20, pady = 20, sticky= "nsew")

        self.about_us_frame.grid_columnconfigure(0, weight = 1)
        self.about_us_frame.grid_rowconfigure(5, weight = 1)

        self.about_label = ttk.Label(self.about_us_frame, text = "About Us", font= ("Raleway", 18, 'bold'), bootstyle = "inverse-light")
        self.about_label.grid(row = 0, column = 0, pady=(10,5))

        #Text paragraph Frame
        self.paragraph_frame = ttk.Frame(self.about_us_frame, borderwidth=0, bootstyle= 'secondary' )
        self.paragraph_frame.grid(row = 1, column = 0, sticky = 'ew', padx = 10, pady = (5, 20))

        self.paragraph_frame.grid_columnconfigure(0, weight = 1)
        self.paragraph_frame.grid_rowconfigure(0, weight = 1)

        #text paragraph
        self.paragraph_label = ttk.Label(self.paragraph_frame, text= "Welcome to Gait Insight, the premier tool for healthcare practitioners conducting gait assessments. \nOur application is meticulously designed to provide comprehensive and invaluable information about gait\npatterns,empowering healthcare professionals to conduct thorough evaluations and deliver personalized\ncare to their patients."
                                         , font=('raleway', 10), bootstyle = 'inverse-secondary')
        self.paragraph_label.grid(row = 0, column = 0, padx = 15, pady= (10, 10))

        #title label
        self.Title_text = ttk.Label(self.about_us_frame, text= 'Our Team', font= ('raleway', 18, 'bold'), bootstyle = 'inverse-light')
        self.Title_text.grid(row = 2, column = 0, pady=(10,5))

        #frame picture adviser
        self.picture_frame = ttk.Frame(self.about_us_frame, borderwidth= 0, bootstyle = 'light')
        self.picture_frame.grid(row = 3, column = 0, pady= (5, 10))

        #research adviser
        self.research_ad = ttk.Label(self.picture_frame, text="", image= self.master.research_ad, bootstyle = 'inverse-light')
        self.research_ad.grid(row = 0 , column = 0, pady=(10, 3))
        self.research_ad_name = ttk.Label(self.picture_frame, text="Engr. Diana Rose Tambogon", bootstyle = 'inverse-light', font=('montserrat', 8, 'bold'))
        self.research_ad_name.grid(row = 1 , column = 0, pady=(3,0))
        self.research_ad_mail = ttk.Label(self.picture_frame, text="dummyAccount@gmail.com", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.research_ad_mail.grid(row = 2 , column = 0, pady=(3,0))
        self.research_ad_number = ttk.Label(self.picture_frame, text="09083160187", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.research_ad_number.grid(row = 3 , column = 0, pady=(5,10))

        #picture frame members
        self.picture_frame_members = ttk.Frame(self.about_us_frame, borderwidth= 0, bootstyle = 'light')
        self.picture_frame_members.grid(row = 4, column = 0, pady= (0, 10))


        #dale
        self.box_dale = ttk.Frame(self.picture_frame_members, bootstyle = 'light')
        self.box_dale.grid(row = 0, column = 0, padx = 3, pady = 5)

        self.dale_p = ttk.Label(self.box_dale, text="", image= self.master.dale, bootstyle = 'inverse-light')
        self.dale_p.grid(row = 0 , column = 0, padx = 5, pady=(10, 5))
        self.dale_p_name = ttk.Label(self.box_dale, text="Dale M. Panganiban", bootstyle = 'inverse-light', font=('montserrat', 8, 'bold'))
        self.dale_p_name.grid(row = 1 , column = 0, padx = 5, pady=(3,0))
        self.dale_p_text = ttk.Label(self.box_dale, text="panganisbandalem@gmail.com", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.dale_p_text.grid(row = 2, column = 0, padx = 5, pady=(3,0))
        self.dale_p_number = ttk.Label(self.box_dale, text="09560726362", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.dale_p_number.grid(row = 3, column = 0, padx = 5, pady=(5,10))

        #palacio
        self.box_palacio = ttk.Frame(self.picture_frame_members, bootstyle = 'light')
        self.box_palacio.grid(row = 0, column = 1, pady = 5)

        self.john_p = ttk.Label(self.box_palacio, text="", image= self.master.palacio, bootstyle = 'inverse-light')
        self.john_p.grid(row = 0 , column = 0, padx = 5, pady=(10, 5))
        self.john_p_name = ttk.Label(self.box_palacio, text="John Isa Palacio", bootstyle = 'inverse-light', font=('montserrat', 8, 'bold'))
        self.john_p_name.grid(row = 1 , column = 0, padx = 5, pady=(3,0))
        self.john_p_text = ttk.Label(self.box_palacio, text="palacioisammsu@gmail.com", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.john_p_text .grid(row = 2, column = 0, padx = 5, pady=(3,0))
        self.john_p_number = ttk.Label(self.box_palacio, text="09276037739", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.john_p_number.grid(row = 3, column = 0, padx = 5, pady=(5,10))

        #ponce
        self.box_ponce = ttk.Frame(self.picture_frame_members, bootstyle = 'light')
        self.box_ponce.grid(row = 0, column = 2, pady = 5)

        self.yan_p = ttk.Label(self.box_ponce, text="", image= self.master.ponce, bootstyle = 'inverse-light')
        self.yan_p.grid(row = 0 , column = 0, padx = 5, pady=(10, 5))
        self.yan_p_name = ttk.Label(self.box_ponce, text="Selwyne Christian E. Ponce", bootstyle = 'inverse-light', font=('montserrat', 8, 'bold'))
        self.yan_p_name.grid(row = 1 , column = 0, padx = 5, pady=(3,0))
        self.yan_p_text = ttk.Label(self.box_ponce, text="selwyneponce1228@gmail.com", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.yan_p_text .grid(row = 2, column = 0, padx = 5, pady=(3,0))
        self.yan_p_number = ttk.Label(self.box_ponce, text="09083160187", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.yan_p_number.grid(row = 3, column = 0, padx = 5, pady=(5,10))

        #Ay Ay
        self.box_ay = ttk.Frame(self.picture_frame_members, bootstyle = 'light')
        self.box_ay.grid(row = 0, column = 3, pady = 5)

        self.ay_ay = ttk.Label(self.box_ay, text="", image= self.master.ismael, bootstyle = 'inverse-light')
        self.ay_ay.grid(row = 0 , column = 0, padx = 5, pady=(10, 5))
        self.ay_ay_name = ttk.Label(self.box_ay, text="Ismael S. Ay Ay", bootstyle = 'inverse-light', font=('montserrat', 8, 'bold'))
        self.ay_ay_name.grid(row = 1 , column = 0, padx = 5, pady=(3,0))
        self.ay_ay_text = ttk.Label(self.box_ay, text="ismaelsenica@gmail.com", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.ay_ay_text .grid(row = 2, column = 0, padx = 5, pady=(3,0))
        self.ay_ay_number = ttk.Label(self.box_ay, text="09068840451", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.ay_ay_number.grid(row = 3, column = 0, padx = 5, pady=(5,10))

        #salmo
        self.box_salmo = ttk.Frame(self.picture_frame_members, bootstyle = 'light')
        self.box_salmo.grid(row = 0, column = 4, pady = 5)

        self.salmo = ttk.Label(self.box_salmo, text="", image= self.master.salmo, bootstyle = 'inverse-light')
        self.salmo.grid(row = 0 , column = 0, padx = 5, pady=(10, 5))
        self.salmo_name = ttk.Label(self.box_salmo, text="Lanz Brent Salmo", bootstyle = 'inverse-light', font=('montserrat', 8, 'bold'))
        self.salmo_name.grid(row = 1 , column = 0, padx = 5, pady=(3,0))
        self.salmo_text = ttk.Label(self.box_salmo, text="lanzbrent08@gmail.com", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.salmo_text .grid(row = 2, column = 0, padx = 5, pady=(3,0))
        self.salmo_number = ttk.Label(self.box_salmo, text="09083160187", bootstyle = 'inverse-light', font=('montserrat', 8))
        self.salmo_number.grid(row = 3, column = 0, padx = 5, pady=(5,10))
        
    #frame 2 -----> Register Patients
    def reg_Patients(self):
        self.stop_esp()
        self.regpatient_frame = ttk.Frame(self.main_frame, borderwidth=0, bootstyle= 'light')
        self.regpatient_frame.grid(row = 0, column = 0, padx = 20, pady = 20, sticky= "nsew")

        self.regpatient_frame.grid_columnconfigure(0, weight = 1)
        self.regpatient_frame.grid_rowconfigure(3, weight = 1)

        self.reg_label = ttk.Label(self.regpatient_frame, text = "Register Patient Section", font= ("Raleway", 18, 'bold'), bootstyle = "inverse-light")
        self.reg_label.grid(row = 0, column = 0, pady=(20,10))

        self.search_bar_frame = ttk.Frame(self.regpatient_frame, borderwidth = 0, bootstyle = "light")
        self.search_bar_frame.grid(row = 1 , column = 0, sticky="w")

        self.search_entry = ttk.Entry(self.search_bar_frame, font= ('montserrat', 12, 'bold'), bootstyle = 'default', width = 30)
        self.search_entry.pack(side = tk.LEFT, padx =(20, 10), pady = 10)

        #search bar icon
        self.search_bar_icon = ttk.Button(self.search_bar_frame, text="", image= self.master.search_icon, cursor = "hand2", takefocus= False, command=self.search_patient)
        self.search_bar_icon.pack(side = tk.LEFT, padx = 10, pady = 30)

        #register button frame
        self.add_button_frame = ttk.Frame(self.regpatient_frame, borderwidth= 0, bootstyle = 'light')
        self.add_button_frame.grid(row = 1 , column = 0, sticky="e", padx= 20, pady = (20, 20))

        self.modify_button = ttk.Button(self.add_button_frame, text= "Modify", width= 7, 
                                         style= 'main.TButton', takefocus= False, cursor= 'hand2',
                                         command = self.open_update_window)
        self.modify_button.pack(side = tk.RIGHT, padx = (20, 5))

        self.add_button = ttk.Button(self.add_button_frame, text= "ADD", width= 7, 
                                         style= 'main.TButton', takefocus= False, cursor= 'hand2', 
                                         command = lambda:self.master.open_popupWindow(popupWindow_register_add))
        self.add_button.pack(side = tk.RIGHT, padx = (5, 20))

        #Table Widget
        self.table_frame = ttk.Frame(self.regpatient_frame, borderwidth= 0, bootstyle = 'secondary')
        self.table_frame.grid(row = 2, column= 0, sticky = "nsew", padx = 20, pady = (0,10))
        self.table_frame.grid_columnconfigure(0, weight = 1)
        self.table_frame.grid_rowconfigure(0, weight = 1)

        self.table_register_patient = ttk.Treeview(self.table_frame, columns = ('Client-ID','FName', 'LName', 'Age', 'Gender', 'Address', 'Birthdate'), 
                                                   show= 'headings', height = 20, bootstyle = "info")
        self.table_register_patient.column('Client-ID', width = 100)
        self.table_register_patient.column('FName', width = 150)
        self.table_register_patient.column('LName', width = 150)
        self.table_register_patient.column('Age', width = 80)
        self.table_register_patient.column('Gender', width = 80)
        self.table_register_patient.column('Address', width = 150)
        self.table_register_patient.column('Birthdate', width = 100)
                         
        self.table_register_patient.heading('Client-ID', text = "Client-ID")
        self.table_register_patient.heading('FName', text = "First Name")
        self.table_register_patient.heading('LName', text = "Last Name")
        self.table_register_patient.heading('Age', text = "Age")
        self.table_register_patient.heading('Gender', text = "Gender")
        self.table_register_patient.heading('Address', text = "Adddress")
        self.table_register_patient.heading('Birthdate', text = "Birthdate")
        self.table_register_patient.grid(row = 0, column= 0, sticky = "nsew", padx = 20, pady = 20)

        self.populate_patient_table()

    def populate_patient_table(self):
        self.table_register_patient.delete(*self.table_register_patient.get_children())

        conn = mysql.connector.connect(
        host = "localhost",
	    user= "gaitrpi",
	    password = "gait123",
	    database="gaitdata"
        )

        cursor = conn.cursor()
        cursor.execute("SELECT client_id, first_name, last_name, age, sex, address, birthdate FROM patient_info")

        for row in cursor.fetchall():
            self.table_register_patient.insert('', 'end', values=row + ('',))

        conn.commit()
        cursor.close()
        conn.close()

    def search_patient(self):
        # Retrieve the search input from the entry widget
        search_text = self.search_entry.get().strip()

        # Clear existing search results
        self.table_register_patient.delete(*self.table_register_patient.get_children())

        if not search_text:
            # If search text is empty, show all patients
            self.populate_patient_table()
            return

        # Connect to the database
        conn = mysql.connector.connect(
            host = "localhost",
	    user= "gaitrpi",
	    password = "gait123",
	    database="gaitdata"
        )

        cursor = conn.cursor()

        # Execute the query to search for patients based on client ID, first name, or last name
        query = ("SELECT client_id, first_name, last_name, age, sex, address, birthdate "
                "FROM patient_info "
                "WHERE client_id = %s OR first_name LIKE %s OR last_name LIKE %s")
        cursor.execute(query, (search_text, f'%{search_text}%', f'%{search_text}%'))

        for row in cursor.fetchall():
            self.table_register_patient.insert('', 'end', values=row + ('',))

        conn.commit()
        cursor.close()
        conn.close()

    def open_update_window(self):
        # Get the selected item from the treeview
        selected_item = self.table_register_patient.focus()
        if selected_item:
            # Extract client_id from the selected row
            client_id = self.table_register_patient.item(selected_item)['values'][0]
            if client_id:
                # Open the update window with the selected client_id
                update_window = popupWindow_register_modify(self.master, client_id)
                update_window.grab_set()  # Make the update window modal

    #Frame 3 ---------------------->
    def Patients_records(self):
        self.stop_esp()
        self.patient_records_frame = ttk.Frame(self.main_frame, borderwidth=0, bootstyle='light')
        self.patient_records_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.patient_records_frame.grid_columnconfigure(0, weight=1)
        self.patient_records_frame.grid_rowconfigure(3, weight=1)

        self.records_label = ttk.Label(self.patient_records_frame, text="Patient Records Section", font=("Raleway", 18, 'bold'), bootstyle="inverse-light")
        self.records_label.grid(row=0, column=0, pady=(20,10))

        self.search_bar_2_frame = ttk.Frame(self.patient_records_frame, borderwidth=0, bootstyle="light")
        self.search_bar_2_frame.grid(row=1, column=0, sticky="w")

        self.search_entry_2 = ttk.Entry(self.search_bar_2_frame, font=('montserrat', 12, 'bold'), bootstyle='default', width=30)
        self.search_entry_2.pack(side=tk.LEFT, padx=(20, 10), pady=30)

        # search bar icon
        self.search_bar_icon = ttk.Button(self.search_bar_2_frame, text="", image=self.master.search_icon, cursor="hand2", takefocus=False, command=self.search_patient2)
        self.search_bar_icon.pack(side=tk.LEFT, padx=10, pady=30)

        # Label for the time range selection
        self.time_range_label = ttk.Label(self.search_bar_2_frame, text="Select Date", font=('Arial', 10), foreground="gray")
        self.time_range_label.pack(side=tk.LEFT, padx=(10, 5), pady=30)

        # Combobox for time range selection
        self.time_range_var = tk.StringVar()
        self.time_range_combobox = ttk.Combobox(self.search_bar_2_frame, textvariable=self.time_range_var, state="readonly", values=['All','Within this day', 'Last Week', 'Last 2 Weeks', 'Last Month', 'Last 6 Months', 'Last Year'])
        self.time_range_combobox.pack(side=tk.LEFT, padx=5, pady=30)
        self.time_range_combobox.bind("<<ComboboxSelected>>", self.update_patient_records)



        # Scrollable Table
        self.scroll_bar_container = ttk.Frame(self.patient_records_frame, borderwidth=0, bootstyle='secondary')
        self.scroll_bar_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.scroll_bar_container.grid_columnconfigure(0, weight=1)
        self.scroll_bar_container.grid_rowconfigure(0, weight=1)

        self.scrollable_frame = ScrolledFrame(self.scroll_bar_container, autohide=False, bootstyle='light-rounded', height=400)
        self.scrollable_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        self.update_patient_records()

    def get_time_range_filter(self):
        selected_range = self.time_range_var.get()
        now = datetime.now()
        start_time = None

        if selected_range == 'All':
            return None  # No filtering needed, return None to indicate no start time

        if selected_range == 'Within this day':
            start_time = now.date()  # Only use the date part
        elif selected_range == 'Last Week':
            start_time = (now - timedelta(days=7)).date()
        elif selected_range == 'Last 2 Weeks':
            start_time = (now - timedelta(days=14)).date()
        elif selected_range == 'Last Month':
            start_time = (now - timedelta(days=30)).date()
        elif selected_range == 'Last 6 Months':
            start_time = (now - timedelta(days=180)).date()
        elif selected_range == 'Last Year':
            start_time = (now - timedelta(days=365)).date()

        print(f"Selected range: {selected_range}, Start time: {start_time}")  # Debug statement
        return start_time


        # Update the view to reflect changes
    def search_patient2(self):
        search_text = self.search_entry_2.get().strip()

        # Clear existing patient assessments
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        if not search_text:
            self.update_patient_records()
            return

        try:
            # Fetch filtered assessment records based on the search criteria (client ID)
            query = "SELECT a.client_id, a.date_time, a.assessment_num, p.first_name, p.last_name " \
                    "FROM assessment a " \
                    "INNER JOIN patient_info p ON a.client_id = p.client_id " \
                    "WHERE a.client_id = %s OR a.date_time = %s OR assessment_num = %s OR p.first_name like %s OR p.last_name like %s " \
                    "GROUP BY a.date_time,a.assessment_num ORDER BY a.date_time DESC"
            self.cursor.execute(query, (search_text, search_text, search_text,'%'+search_text+'%','%'+search_text+'%'))
            filtered_assessments = self.cursor.fetchall()

            print(f"Filtered assessments fetched: {filtered_assessments}")  # Debug statement

            displayed_records = set()  # Set to track displayed records
            displayed_count = 0  # Counter to track displayed records

            # Iterate over the fetched filtered assessments
            for i, (client_id, date_time, assessment_num, first_name, last_name) in enumerate(filtered_assessments):
                if displayed_count >= 30:
                    break

                record_key = (client_id, date_time, assessment_num, first_name, last_name)

                # Check if this record has already been displayed
                if record_key in displayed_records:
                    continue  # Skip displaying this duplicate record

                # Add record to displayed set
                displayed_records.add(record_key)

                self.display_assessment_record(i, client_id, date_time, assessment_num, first_name, last_name)

                displayed_count += 1  #

        except mysql.connector.Error as e:
            print(f"Error retrieving filtered assessments: {e}")
        self.scrollable_frame.update()

    def populate_patient_assessments(self):
        try:
             # Clear existing patient assessments
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            # Query to fetch assessments for the current patient
            query = "SELECT a.client_id, a.date_time, a.assessment_num, p.first_name, p.last_name " \
                    "FROM assessment a " \
                    "INNER JOIN patient_info p ON a.client_id = p.client_id " \
                    "WHERE p.client_id = %s " \
                    "ORDER BY a.date_time DESC"
            self.cursor.execute(query, (self.client_id,))
            assessments = self.cursor.fetchall()

            displayed_records = set()  # Set to track displayed records
            displayed_count = 0  # Counter to track displayed records per patient

            # Iterate over the fetched assessments
            for i, (client_id, date_time, assessment_num, first_name, last_name) in enumerate(assessments):
                if displayed_count >= 30:
                    break

                record_key = (client_id, date_time, assessment_num, first_name, last_name)

                # Check if this record has already been displayed
                if record_key in displayed_records:
                    continue  # Skip displaying this duplicate record

                # Add record to displayed set
                displayed_records.add(record_key)

                self.display_assessment_record(i, client_id, date_time, assessment_num, first_name, last_name)

                displayed_count += 1  #

        except mysql.connector.Error as e:
            print(f"Error retrieving patient assessments: {e}")
        self.scrollable_frame.update()

    def display_assessment_record(self, row_index, client_id, date_time, assessment_num, first_name, last_name):
        # Create box frame
        self.box_frame = ttk.Frame(self.scrollable_frame, borderwidth=0, bootstyle='info')
        self.box_frame.grid(row=row_index, column=0, padx=15, pady=7, sticky="nsew")

        self.box_frame.grid_columnconfigure(0, weight=1)
        self.box_frame.grid_rowconfigure(0, weight=1)

        # Title of the assessment
        self.assessment_title = ttk.Label(self.box_frame, text=f"Assessment {assessment_num} - {date_time} - {client_id} - {first_name} {last_name}", font=('Montserrat', 10, 'bold'),
                                          bootstyle='inverse-info')
        self.assessment_title.grid(row=0, column=0, padx=30, pady=20)

        # Buttons view and delete
        self.buttons_frame = ttk.Frame(self.box_frame, borderwidth=0, bootstyle='info')
        self.buttons_frame.grid(row=0, column=2, padx=10, pady=0, sticky="w")

        self.view_button = ttk.Button(self.buttons_frame, text="", image=self.master.eye_icon, width=80, cursor="hand2",
                                      takefocus=False, bootstyle="info",
                                      command=lambda id=client_id, num=assessment_num, fname=first_name, lname=last_name, dt=date_time: self.view_assessment(id, num, fname, lname, dt))
        self.view_button.pack(side=tk.LEFT, padx=(280, 10))
        self.delete_button = ttk.Button(self.buttons_frame, text="", image=self.master.delete_icon, width=80,
                                        cursor="hand2", takefocus=False, bootstyle="info", command=lambda id=client_id, num=assessment_num, dt=date_time: self.delete_assessment(id, num, dt))
        self.delete_button.pack(side=tk.LEFT, padx=30)

    def update_patient_records(self, event=None):
        # Clear existing patient assessments
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        time_range_filter = self.get_time_range_filter()
        if time_range_filter:
            query = ("SELECT DISTINCT a.client_id, a.date_time, a.assessment_num, p.first_name, p.last_name "
                    "FROM assessment a "
                    "INNER JOIN patient_info p ON a.client_id = p.client_id "
                    "WHERE DATE(a.date_time) >= %s "
                    "ORDER BY a.date_time DESC LIMIT 30")
            self.cursor.execute(query, (time_range_filter,))
        else:
            query = ("SELECT DISTINCT a.client_id, a.date_time, a.assessment_num, p.first_name, p.last_name "
                    "FROM assessment a "
                    "INNER JOIN patient_info p ON a.client_id = p.client_id "
                    "ORDER BY a.date_time DESC LIMIT 30")
            self.cursor.execute(query)

        assessments = self.cursor.fetchall()
        print(f"Assessments fetched: {assessments}")  # Debug statement

        displayed_records = set()  # Set to track displayed records
        displayed_count = 0  # Counter to track displayed records per patient

        for i, (client_id, date_time, assessment_num, first_name, last_name) in enumerate(assessments):
            if displayed_count >= 30:
                break  # Stop displaying records once 30 records have been displayed

            record_key = (client_id, date_time, assessment_num, first_name, last_name)

            # Check if this record has already been displayed
            if record_key in displayed_records:
                continue  # Skip displaying this duplicate record

            # Add record to displayed set
            displayed_records.add(record_key)

            self.display_assessment_record(i, client_id, date_time, assessment_num, first_name, last_name)

            displayed_count += 1  # Increment the displayed count

        self.scrollable_frame.update()



    def delete_assessment(self, client_id, assessment_num, date_time):
        # Construct the confirmation message with formatted strings
        confirmation_message = f"Are you sure you want to delete assessment number {assessment_num} of client {client_id} on {date_time}?"

        # Display a confirmation popup dialog
        confirmation = messagebox.askyesno("Confirm Deletion", confirmation_message)

        if confirmation:
            try:
                # Construct the DELETE query to remove the assessment record
                delete_query = "DELETE FROM assessment WHERE client_id = %s AND assessment_num = %s AND date_time = %s"
                self.cursor.execute(delete_query, (client_id, assessment_num, date_time))
                self.conn.commit()  # Commit the transaction

                print(f"Assessment with Client ID {client_id}, Assessment Number {assessment_num}, and Date {date_time} deleted successfully.")

                # Clear the existing assessments and repopulate the frame
                self.populate_patient_assessments()  # Repopulate the assessments after deletion
            except mysql.connector.Error as err:
                print(f"Error deleting assessment: {err}")
        else:
            print("Deletion canceled by user.")
            
    def view_assessment(self, client_id, assessment_num, first_name, last_name, dt):
        # Instantiate popupWindow_Table and pass client_id to it
        self.master.open_popupWindow2(patient_records, client_id, assessment_num, first_name, last_name, dt)

class popupWindow_register_add(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        size = [420, 550]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title('Register Patient')

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.info_frame = ttk.Frame(self, borderwidth= 0, bootstyle = "light")
        self.info_frame.grid(row= 0, column = 0)

        self.resizable(False, False)

        #Frames ------------>
        self.reg_label = ttk.Label(self.info_frame, text = "Register Patient", font= ("Raleway", 18, 'bold'), bootstyle = "inverse-light")
        self.reg_label.grid(row = 0, column = 0, padx = 10, pady=(20,10))

        self.Fname_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.Fname_frame.grid(row = 1, column = 0, padx = 10, pady=(20,10))

        self.Lname_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.Lname_frame.grid(row = 2, column = 0, padx = 10, pady=(10,10))

        self.age_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.age_frame.grid(row = 3, column = 0, padx = 10, pady=(10,10))

        self.address_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.address_frame.grid(row = 6, column = 0, padx = 10, pady=(10,10))

        self.Bdate_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.Bdate_frame.grid(row = 5, column = 0, padx = 10, pady=(10,10))

        self.gender_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.gender_frame.grid(row = 4, column = 0, padx = 10, pady=(10,10))
        #end ------------>

        #elements
        self.Fname_label = ttk.Label(self.Fname_frame, text = "First Name: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.Fname_label.pack(side= tk.LEFT, padx = (10, 5))
        self.Fname_entry = ttk.Entry(self.Fname_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.Fname_entry.pack(side= tk.LEFT, padx = (5, 10))

        self.Lname_label = ttk.Label(self.Lname_frame, text = "Last Name: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.Lname_label.pack(side= tk.LEFT, padx = (10, 5))
        self.Lname_entry = ttk.Entry(self.Lname_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.Lname_entry.pack(side= tk.LEFT, padx = (5, 10))

        self.age_label = ttk.Label(self.age_frame, text = "Age: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.age_label.pack(side= tk.LEFT, padx = (10, 30))
        self.age_entry = ttk.Entry(self.age_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.age_entry.pack(side= tk.LEFT, padx = (30, 10))
        
        self.gender_label = ttk.Label(self.gender_frame, text = "Gender: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.gender_label.pack(side= tk.LEFT, padx = (10, 18))
        self.gender = ttk.Combobox(self.gender_frame, values=["Male", "Female"], bootstyle = 'primary', width= 19,  font= ('montserrat', 10, 'bold'))
        self.gender.pack(side= tk.LEFT, padx = (18, 10))

        self.address_label = ttk.Label(self.address_frame, text = "Address: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.address_label.pack(side= tk.LEFT, padx = (10, 13))
        self.address_entry = ttk.Entry(self.address_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.address_entry.pack(side= tk.LEFT, padx = (13, 10))

        self.Bdate_label = ttk.Label(self.Bdate_frame, text = "Birthdate: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.Bdate_label.pack(side= tk.LEFT, padx = (10, 12))
        self.bdate = ttk.DateEntry(self.Bdate_frame, bootstyle='primary', width= 17, dateformat='%d/%m/%Y')
        self.bdate.pack(side= tk.LEFT, padx = (12, 10)) 

        self.submit_button = ttk.Button(self.info_frame, text= "Register Patient", command=self.add_patient
                                         , style= 'main.TButton', takefocus= False, cursor= 'hand2')
        self.submit_button.grid(row=7, column=0, padx=10, pady=(30, 60))

        self.popup_window_calendar = None

        self.submit_button.configure(command=self.add_patient)

    def add_patient(self):
        # Retrieve data from entry fields
        first_name = self.Fname_entry.get()
        last_name = self.Lname_entry.get()
        age = self.age_entry.get()
        address = self.address_entry.get()
        gender = self.gender.get()
        birthdate_entry = self.bdate.entry.get()  

        
        birthdate = datetime.strptime(birthdate_entry, "%d/%m/%Y").strftime("%Y-%m-%d")

        if all([first_name, last_name, age, address, gender, birthdate]):
            conn = mysql.connector.connect(
                host = "localhost",
	        user= "gaitrpi",
	        password = "gait123",
	        database="gaitdata"
            )

            cursor = conn.cursor()
            try:
                sql = "INSERT INTO patient_info (first_name, last_name, age, sex, address, birthdate) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (first_name, last_name, age, gender, address, birthdate)
                cursor.execute(sql, values)
                conn.commit()

                cursor.close()
                conn.close()

                self.clear_entry_fields()
                self.destroy()
                print("Patient added successfully!")
            except mysql.connector.Error as err:
                print(f"Error: {err}")

    def clear_entry_fields(self):
        self.Fname_entry.delete(0, 'end')
        self.Lname_entry.delete(0, 'end')
        self.age_entry.delete(0, 'end')
        self.address_entry.delete(0, 'end')
        self.bdate.entry.delete(0, 'end')


class popupWindow_register_modify(tk.Toplevel):
    def __init__(self, parent,client_id):
        super().__init__(parent)
        self.client_id = client_id

        size = [420, 550]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title('Modify Patient')

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.info_frame = ttk.Frame(self, borderwidth= 0, bootstyle = "light")
        self.info_frame.grid(row= 0, column = 0)

        self.resizable(False, False)

        #Frames ------------>
        self.reg_label = ttk.Label(self.info_frame, text = "Modify Patient", font= ("Raleway", 18, 'bold'), bootstyle = "inverse-light")
        self.reg_label.grid(row = 0, column = 0, padx = 10, pady=(20,10))

        self.Fname_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.Fname_frame.grid(row = 1, column = 0, padx = 10, pady=(20,10))

        self.Lname_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.Lname_frame.grid(row = 2, column = 0, padx = 10, pady=(10,10))

        self.age_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.age_frame.grid(row = 3, column = 0, padx = 10, pady=(10,10))

        self.address_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.address_frame.grid(row = 6, column = 0, padx = 10, pady=(10,10))

        self.Bdate_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.Bdate_frame.grid(row = 5, column = 0, padx = 10, pady=(10,10))

        self.gender_frame = ttk.Frame(self.info_frame, borderwidth= 0, bootstyle = "light")
        self.gender_frame.grid(row = 4, column = 0, padx = 10, pady=(10,10))
        #end ------------>

        #elements
        self.Fname_label = ttk.Label(self.Fname_frame, text = "First Name: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.Fname_label.pack(side= tk.LEFT, padx = (10, 5))
        self.Fname_entry = ttk.Entry(self.Fname_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.Fname_entry.pack(side= tk.LEFT, padx = (5, 10))

        self.Lname_label = ttk.Label(self.Lname_frame, text = "Last Name: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.Lname_label.pack(side= tk.LEFT, padx = (10, 5))
        self.Lname_entry = ttk.Entry(self.Lname_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.Lname_entry.pack(side= tk.LEFT, padx = (5, 10))

        self.age_label = ttk.Label(self.age_frame, text = "Age: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.age_label.pack(side= tk.LEFT, padx = (10, 30))
        self.age_entry = ttk.Entry(self.age_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.age_entry.pack(side= tk.LEFT, padx = (30, 10))
        
        self.gender_label = ttk.Label(self.gender_frame, text = "Gender: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.gender_label.pack(side= tk.LEFT, padx = (10, 18))
        self.gender = ttk.Combobox(self.gender_frame, values=["Male", "Female"], bootstyle = 'primary', width= 19,  font= ('montserrat', 10, 'bold'))
        self.gender.pack(side= tk.LEFT, padx = (18, 10))

        self.address_label = ttk.Label(self.address_frame, text = "Address: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.address_label.pack(side= tk.LEFT, padx = (10, 13))
        self.address_entry = ttk.Entry(self.address_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.address_entry.pack(side= tk.LEFT, padx = (13, 10))

        self.Bdate_label = ttk.Label(self.Bdate_frame, text = "Birthdate: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.Bdate_label.pack(side= tk.LEFT, padx = (10, 12))
        self.bdate = ttk.DateEntry(self.Bdate_frame, bootstyle='primary', width=17, dateformat='%Y-%m-%d')
        self.bdate.pack(side= tk.LEFT, padx = (12, 10))

        self.submit_button = ttk.Button(self.info_frame, text= "Modify Patient", command= self.update_patient
                                         , style= 'main.TButton', takefocus= False, cursor= 'hand2')
        self.submit_button.grid(row=7, column=0, padx=10, pady=(30, 60))

        self.load_patient_data()


    def load_patient_data(self):
        conn = mysql.connector.connect(
            host = "localhost",
	    user= "gaitrpi",
            password = "gait123",
	    database="gaitdata"
        )

        cursor = conn.cursor()
        try:
            sql = "SELECT first_name, last_name, age, birthdate, sex, address FROM patient_info WHERE client_id = %s"
            cursor.execute(sql, (self.client_id,))
            patient_data = cursor.fetchone()

            if patient_data:
                first_name, last_name, age, birthdate, sex, address = patient_data
                self.Fname_entry.insert(0, first_name)
                self.Lname_entry.insert(0, last_name)
                self.age_entry.insert(0, age)
                
                # Format birthdate from datetime.date object to '%d/%m/%Y' format
                formatted_birthdate = birthdate.strftime('%d/%m/%Y')
                
                # Clear birthdate field before inserting
                self.bdate.entry.delete(0, 'end')
                self.bdate.entry.insert(0, formatted_birthdate)
                
                self.gender.set(sex)
                self.address_entry.insert(0, address)
            else:
                print(f"No patient found with client_id = {self.client_id}")

            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error retrieving patient data: {err}")

        cursor.close()
        conn.close()

    def update_patient(self):
        # Retrieve data from entry fields
        first_name = self.Fname_entry.get()
        last_name = self.Lname_entry.get()
        age = self.age_entry.get()
        birthdate_entry = self.bdate.entry.get()
        birthdate = datetime.strptime(birthdate_entry, "%d/%m/%Y").strftime("%Y-%m-%d")
        address = self.address_entry.get()
        gender = self.gender.get()


        if all([first_name, last_name, age, birthdate, address, gender]):
            conn = mysql.connector.connect(
                host = "localhost",
	        user= "gaitrpi",
	        password = "gait123",
	        database="gaitdata"
            )

            cursor = conn.cursor()
            try:
                sql = "UPDATE patient_info SET first_name = %s, last_name = %s, age = %s, birthdate = %s, sex = %s, address = %s WHERE client_id = %s"
                values = (first_name, last_name, age, birthdate, gender, address, self.client_id)
                cursor.execute(sql, values)
                conn.commit()

                cursor.close()
                conn.close()

                print("Patient updated successfully!")
                self.destroy()  # Close the update window after successful update
            except mysql.connector.Error as err:
                print(f"Error updating patient data: {err}")
        else:
            print("Please fill in all fields before updating.")

        
class Account_Settings(tk.Toplevel):
    def __init__(self, parent, db_connection):
        super().__init__(parent)
        self.parent = parent
        self.db_connection = db_connection

        size = [400, 350]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)
        self.title('Account Settings')

        self.resizable(False, False)

        #Main Account Frame
        self.account_settings_frame = ttk.Frame(self, borderwidth= 0, bootstyle="light") 
        self.account_settings_frame.grid(row = 0, column= 0, padx = 20, pady = 20)

        #Frames ------------>
        self.reg_label = ttk.Label(self.account_settings_frame, text = "Account Settings", font= ("Raleway", 20, 'bold'), bootstyle = "inverse-light")
        self.reg_label.grid(row = 0, column = 0, padx = 10, pady=(20,10))

        self.pin_orig_frame = ttk.Frame(self.account_settings_frame, borderwidth= 0, bootstyle = "light")
        self.pin_orig_frame.grid(row = 1, column = 0, padx = 10, pady=(20,10))

        self.pin_new_frame = ttk.Frame(self.account_settings_frame, borderwidth= 0, bootstyle = "light")
        self.pin_new_frame.grid(row = 2, column = 0, padx = 10, pady=(10,20))

        #elements
        self.pin_orig_label = ttk.Label(self.pin_orig_frame, text = "Original Pin: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.pin_orig_label.pack(side= tk.LEFT, padx = (10, 5))
        self.pin_orig_entry = ttk.Entry(self.pin_orig_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.pin_orig_entry.pack(side= tk.LEFT, padx = (5, 10))

        self.pin_new_label = ttk.Label(self.pin_new_frame, text = "New Pin: ", font=('montserrat', 10, 'bold'), bootstyle = 'inverse-light')
        self.pin_new_label.pack(side= tk.LEFT, padx = (10, 19))
        self.pin_new_entry = ttk.Entry(self.pin_new_frame, width = 20, font=('montserrat', 10, 'bold'), bootstyle= 'primary')
        self.pin_new_entry.pack(side= tk.LEFT, padx = (19, 10))

        #submit button
        self.change_button = ttk.Button(self.account_settings_frame, text= "Change Password", command=self.change_password
                                         , style= 'main.TButton', takefocus= False, cursor= 'hand2')
        self.change_button.grid(row= 3, column=0, padx=10, pady=(10, 30))
        
        

    def change_password(self):
        old_pin = self.pin_orig_entry.get()  
        new_pin = self.pin_new_entry.get() 

        if old_pin == "" or new_pin == "":
            self.show_message("Please enter both old and new PIN.")
            return

        if not self.validate_pin(old_pin):
            self.show_message("Invalid old PIN.")
            return

        self.update_pin(old_pin, new_pin)
    
    def validate_pin(self, pin):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM pin WHERE pin = %s", (pin,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    
    def update_pin(self, old_pin, new_pin):
        cursor = self.db_connection.cursor()
        update_query = "UPDATE pin SET pin = %s WHERE pin = %s"
        cursor.execute(update_query, (new_pin, old_pin))
        self.db_connection.commit()
        cursor.close()
        self.show_message("PIN updated successfully.")
        self.destroy()

    def show_message(self, message):
        messagebox.showinfo("Message", message)

def validate_pin(pin):
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM pin WHERE pin = %s', (pin,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

class Side_Cam(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)
       
        self.left_frame_timestamp = []
        self.right_frame_timestamp = []
        self.esp_data_left = []
        self.esp_data_right = []
        self.master.synced_right.clear()
        self.master.synced_left.clear()
        self.style = style

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        #camera part
        self.assessment_state = ''
        self.assessment_state_text = 'None'
        
        self.frame_number = 0
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)  # Reduced frame width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)  # Reduced frame height
        self.recording = False
        self.out = None

        #create a container frame 
        self.container_frame = ttk.Frame(self, borderwidth= 0, bootstyle= 'light')
        self.container_frame.grid(row = 0, column = 0, padx = 5, pady = 5, sticky= "nsew")

        self.container_frame.grid_columnconfigure(0, weight = 1)
        self.container_frame.grid_rowconfigure(0, weight = 1)

        #create a text Frame
        self.text_frame = ttk.Frame(self.container_frame, borderwidth=0, bootstyle = "light")
        self.text_frame.grid(row = 0, column = 0, padx = 20)

        #create a frame for web cam
        self.web_cam_frame = ttk.Frame(self.container_frame, borderwidth=0, bootstyle = "light")
        self.web_cam_frame.grid(row = 1, column = 0)
        #create a frame for buttons
        self.choose_buttons_frame = ttk.Frame(self.container_frame, borderwidth=0, bootstyle = "light")
        self.choose_buttons_frame.grid(row = 2, column = 0, pady = 5, padx = 20)

        #current Patient Label and Current Video
        self.current_patient = ttk.Label(self.text_frame, text = f"Current Patient: {self.master.current_patient}", font= ("montserrat", 12, 'bold'), bootstyle = "inverse-light")
        self.current_patient.grid(row = 0, column = 0, padx = (0, 120))
        self.current_leg = ttk.Label(self.text_frame, text = f"Current Video: {self.assessment_state_text}", font=("montserrat", 12, 'bold'), bootstyle = "inverse-light")
        self.current_leg.grid(row = 0, column = 2, padx = (120, 0))

        #choose side button
        self.right_button = ttk.Button(self.choose_buttons_frame, text= "START RIGHT LEG", width = 15, style = 'main.TButton', takefocus= False,
                                          cursor = "hand2", command= lambda: self.change_button('right'))
        self.right_button.grid(row = 0, column = 0, padx = (0, 20))
        self.leg_button = ttk.Button(self.choose_buttons_frame, text= "START LEFT LEG", width = 15, style = 'main.TButton', takefocus= False,
                                          cursor = "hand2", command= lambda: self.change_button('left'))
        self.leg_button.grid(row = 0, column = 1, padx = (20, 20))
        self.back_button = ttk.Button(self.choose_buttons_frame, text= "EXIT", width = 15, style = 'danger.TButton', takefocus= False,
                                          cursor = "hand2", command= lambda: self.master.change_frame(self, MenuBar))
        self.back_button.grid(row = 0, column = 2, padx = (20, 0))
        
        #video 
        self.camera_thread = threading.Thread(target=self.camera_update_thread, daemon=True)
        self.camera_thread.start()
        
        self.clear_folder('Data_process/Left_frames')
        self.clear_folder('Data_process/Right_frames')
        self.reference_timer = 0

         #mqtt Connection
        self.client = mqtt.Client("rpi_client1")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.message_callback_add('esp32/sensor1', self.callback_esp32_sensor1)
        self.client.message_callback_add('esp32/sensor2', self.callback_esp32_sensor2)
        #placed into left/right logic
        self.client.message_callback_add('rpi/broadcast', self.callback_rpi_broadcast)
        self.client_subscriptions(self.client)
        self.client.connect('192.168.0.143',1883) # connect to mqtt
        self.client.loop_start()
        
        
    def clear_folder(self, folder_path):
        # List all items in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            
            # Check if it's a file or directory
            if os.path.isfile(item_path):
                
                os.remove(item_path)

    #use only for mqtt here 
    def on_connect(self, client, userdata, flags, rc):
        self.client_subscriptions(self.client)
        print("Connected to MQTT server")

    def on_disconnect(self, client, userdata, rc):
        print("Disconnected from MQTT server")
    
    def enter_key(self, msg): #send timestamp to esp32 for syncing        
        pubMsg = self.client.publish(
            topic='rpi/broadcast',
            payload=msg.encode('utf-8'),
            qos=0,
        )
    def right_focus_sensor(self):
        self.client.message_callback_add('esp32/sensor1', self.callback_esp32_sensor1)
        self.client.message_callback_remove('esp32/sensor2')
    def left_focus_sensor(self):
        self.client.message_callback_add('esp32/sensor2', self.callback_esp32_sensor2)
        self.client.message_callback_remove('esp32/sensor1')
                    
    def callback_esp32_sensor1(self, client, userdata, msg):
        #this is where I would save the esp data to dictionary where in the key is frame and the out is esp, example: {55: espdata}
        self.receive_insole(msg.payload.decode('utf-8'))

    def callback_esp32_sensor2(self, client, userdata, msg):
        self.receive_insole(msg.payload.decode('utf-8'))
        
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
    
            self.choose_buttons_frame.grid_forget()
            self.current_leg.config(text=f"Current Video: {self.assessment_state_text}")

            self.record_frame = ttk.Frame(self.container_frame, borderwidth=0, bootstyle = 'primary')
            self.record_frame.grid(row=2, column=0, sticky= "ew", padx= 200)

            self.record_frame.grid_columnconfigure(0, weight = 1)
            self.record_frame.grid_rowconfigure(0, weight = 1)

            self.record_label = ttk.Label(self.record_frame, text= "Press Space to Start Recording", font = ("montserrat", 12, 'bold'), bootstyle = "inverse-primary")
            self.record_label.grid(row = 0, column = 0, pady = 5)
            
            # Bind space key to toggle recording
            self.master.bind('<space>', lambda event: self.toggle_recording(state))
        
        if state == 'left':
            self.master.side_state['Left'] = 1
            self.assessment_state_text = 'Left'
       
            self.choose_buttons_frame.grid_forget()
            self.current_leg.config(text=f"Current Video: {self.assessment_state_text}")

            self.record_frame = ttk.Frame(self.container_frame, borderwidth=0, bootstyle = 'primary')
            self.record_frame.grid(row=2, column=0, sticky= "ew",padx= 200)

            self.record_frame.grid_columnconfigure(0, weight = 1)
            self.record_frame.grid_rowconfigure(0, weight = 1)

            self.record_label = ttk.Label(self.record_frame, text= "Press Space to Start Recording", font = ("montserrat", 12, 'bold'), bootstyle = "inverse-primary")
            self.record_label.grid(row = 0, column = 0, pady = 5)
            
            # Bind space key to toggle recording
            self.master.bind('<space>', lambda event: self.toggle_recording(state))
        
        elif state == 'choose_other':
            
            self.record_frame.grid_forget()
            
            if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
                self.choose_buttons_frame_2 = ttk.Frame(self.container_frame, borderwidth=0, bootstyle = "light")
                self.choose_buttons_frame_2.grid(row = 2, column = 0, pady = 20, padx = 20)

                self.leg_button = ttk.Button(self.choose_buttons_frame_2, text= "START LEFT LEG", width = 15, style = 'main.TButton', takefocus= False,
                                          cursor = "hand2",  command= lambda: self.change_button('left'))
                self.leg_button.grid(row = 0, column = 0, padx = (0, 20))

                self.end_button = ttk.Button(self.choose_buttons_frame_2, text= "END VIDEO TAKING", width = 18, style = 'main.TButton', takefocus= False,
                                          cursor = "hand2", command= lambda: self.after(20, lambda:self.master.change_frame(self, Process_Table)))
                self.end_button.grid(row = 0, column = 1, padx = (20, 20))

                self.back_button = ttk.Button(self.choose_buttons_frame_2, text= "EXIT", width = 15, style = 'danger.TButton', takefocus= False,
                                          cursor = "hand2", command= lambda: self.master.change_frame(self, MenuBar))
                self.back_button.grid(row = 0, column = 2, padx = (20, 0))
            
            elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:

                self.choose_buttons_frame_2 = ttk.Frame(self.container_frame, borderwidth=0, bootstyle = "light")
                self.choose_buttons_frame_2.grid(row = 2, column = 0, pady = 20, padx = 20)

                self.leg_button = ttk.Button(self.choose_buttons_frame_2, text= "START RIGHT LEG", width = 15, style = 'main.TButton', takefocus= False,
                                          cursor = "hand2",  command= lambda: self.change_button('right'))
                self.leg_button.grid(row = 0, column = 0, padx = (0, 20))

                self.end_button = ttk.Button(self.choose_buttons_frame_2, text= "END VIDEO TAKING", width = 18, style = 'main.TButton', takefocus= False,
                                          cursor = "hand2", command= lambda: self.after(20, lambda:self.master.change_frame(self, Process_Table)))
                self.end_button.grid(row = 0, column = 1, padx = (20, 20))

                self.back_button = ttk.Button(self.choose_buttons_frame_2, text= "EXIT", width = 15, style = 'danger.TButton', takefocus= False,
                                          cursor = "hand2", command= lambda: self.master.change_frame(self, MenuBar))
                self.back_button.grid(row = 0, column = 2, padx = (20, 0))

            elif self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 1:
                self.master.change_frame(self, Process_Table)

    def toggle_recording(self, state):
        try:
            if not self.recording:
                self.recording = True
                self.record_label.configure(text="Press Stop to Start Recording")
                self.frame_number = 0
                if self.assessment_state == 'left':
                    self.left_focus_sensor()
                if self.assessment_state == 'right':
                    self.right_focus_sensor()
                self.reference_timer = time.time()
                self.enter_key("Start")  #send start signal to esp32
                
            else:

                #self.enter_key(Request_Data) #request data from esp32  
                # self.client.disconnect() #disconnect
                # self.client.loop_stop()
                #state is 'left' or 'right'
                self.recording = False
                self.enter_key("Stop") #stop recieving signals from esp
                self.record_label.config(text="<Space> to Start Recording")
                # Frame Number go back to 0
                self.change_button('choose_other')

        except Exception as e:
            print("Error", f"An error occurred: {str(e)}")
            # Release resources if an error occurs
            if self.out is not None:
                self.out.release()
                self.out = None

    def receive_insole(self, espdata):
        
        if self.recording:
            if self.assessment_state == 'left':
                self.esp_data_left.append(espdata)
                print(f"Left: {espdata}")
                
            else:
                self.esp_data_right.append(espdata)
                print(f"Right: {espdata}")
    
    def camera_update_thread(self):
        label = ttk.Label(self.web_cam_frame)
        label.grid(row=0, column=0, sticky='nsew')

        def update_frame():
            ret, frame = self.cap.read()
            if ret:
                get_image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                photo = ImageTk.PhotoImage(get_image)
                label.config(image=photo)
                label.image = photo
                
                if label.winfo_exists():
                    label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

                if self.recording:
                    # Save frame as image
                    #TODO: LINK TIMESTAMP TO 
                    cv2.imwrite(f'Data_process/{self.assessment_state_text}_frames/{self.frame_number}.jpg', frame)
                    utc_timestamp = (time.time() - self.reference_timer)*1000
                    if self.assessment_state == 'left':
                        self.left_frame_timestamp.append((self.frame_number,utc_timestamp))
                    if self.assessment_state == 'right':
                        self.right_frame_timestamp.append((self.frame_number,utc_timestamp))
                    self.frame_number += 1

                self.web_cam_frame.update_idletasks()
                self.web_cam_frame.update()
            
            # Schedule the next frame update
            self.web_cam_frame.after(10, update_frame)  # 33 milliseconds ~= 30 fps
                        
        # Start the initial frame update
        update_frame()
        
    def find_closest(self,input_list,reference_list):
        return min(reference_list, key=lambda d: abs(d - input_list))
        
    def sync_timestamp(self,side_camera,side_esp):
        temp_synced_list = []
        side_camera_frame,side_camera_time = map(list,zip(*side_camera))
        if side_esp:
            side_esp_time,side_esp_state = map(list,zip(*side_esp))

            for index, camera_time in enumerate(side_camera_time):
                matched_sensor_time = self.find_closest(camera_time, side_esp_time)
                matched_sensor_index = side_esp_time.index(matched_sensor_time)
                closest_state = side_esp_state[matched_sensor_index]
                if closest_state == 0:
                    closest_state = '000'
                elif closest_state == 1:
                    closest_state = '001'
                elif closest_state == 10:
                    closest_state = '010'
                elif closest_state == 11:
                    closest_state = '011'
                #100 101 and 111 are already proper
                if abs(matched_sensor_time-camera_time) > 80: #when esp delay is greater than specified ms
                    closest_state = "unknown"
                
                #temp_synced_list.append((side_camera_frame[index], str(closest_state),camera_time, matched_sensor_time,abs(matched_sensor_time-camera_time)))
                temp_synced_list.append((side_camera_frame[index], str(closest_state)))
        return temp_synced_list
        
    def destroy(self):
        #sync timestamps
        #print(*self.left_frame_timestamp,sep="\n")
        #print(*self.right_frame_timestamp,sep="\n")
        #print(len(self.esp_data_left))
        if self.left_frame_timestamp: #if left side is recorded
            esp_data_left = list(map(eval,self.esp_data_left))#remove string
            self.master.synced_left = self.sync_timestamp(self.left_frame_timestamp,esp_data_left)
            #print("Left")
            #print(*self.master.synced_left, sep="\n")

        if self.right_frame_timestamp:#if right side is recorded
            esp_data_right= list(map(eval,self.esp_data_right)) #remove string
            self.master.synced_right = self.sync_timestamp(self.right_frame_timestamp,esp_data_right) 
            #print("Right")
            #print(*self.master.synced_right, sep="\n")
        #end syncing
        self.client.disconnect() #disconnect
        self.client.loop_stop()       
        self.camera_thread.join()
        self.cap.release()  
        super().destroy()
        
class patient_records(tk.Toplevel):
    def __init__(self, parent, client_id, assessment_num, first_name, last_name, dt):
        super().__init__(parent)
        self.client_id = client_id
        self.assessment_num = assessment_num
        self.first_name = first_name
        self.last_name = last_name
        self.date = dt
        print(f"Client ID: {client_id}, Assessment Number: {assessment_num} (dt: {dt})")
        self.title('Assessment Table')

        size = [1280,700]
        x = (self.winfo_screenwidth() - size[0]) // 2
        y = (self.winfo_screenheight() - size[1]) // 2

        self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
        self.title('Assessment Table')

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        # Create a frame for the table 
        self.patientTable_frame = ttk.Frame(self, borderwidth=0, bootstyle="light")
        self.patientTable_frame.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        # Configure the grid for the table 
        self.patientTable_frame.grid_rowconfigure(2, weight=1)
        self.patientTable_frame.grid_columnconfigure(0, weight=1)

        # Table title 
        self.tableTitle = ttk.Label(self.patientTable_frame, text=f"{first_name} {last_name} - Assessment Number {assessment_num}", bootstyle='inverse light', font=('Raleway', 18, 'bold'))
        self.tableTitle.grid(row=0, column=0, pady=(20, 20))

        # Tool frames
        self.tool_frame = ttk.Frame(self.patientTable_frame, borderwidth=0, bootstyle="light")
        self.tool_frame.grid(row=1, column=0, sticky="ew", pady=(20, 20))

        # Leg option menu
        self.leg_scroll_label = ttk.Label(self.tool_frame, font=('montserrat', 12, 'bold'), text="Side:", bootstyle= 'inverse-light')
        self.leg_scroll_label.pack(side=tk.LEFT, padx=10)
        self.leg_scroll = ttk.Combobox(self.tool_frame, values=["Right","Left"], bootstyle='primary', width=19, state='readonly', font=('montserrat', 10, 'bold'))
        self.leg_scroll.set("Right")
        self.leg_scroll.pack(side=tk.LEFT, padx=20)

        #Gait phase
        self.leg_phase_label = ttk.Label(self.tool_frame, font=('montserrat', 12, 'bold'), text="Gait Phase:", bootstyle= 'inverse-light')
        self.leg_phase_label.pack(side=tk.LEFT, padx=10)
        self.leg_phase_scroll = ttk.Combobox(self.tool_frame, values=["Initial Contact (1)", "Loading Response (2)", "Midstance (3)", "Terminal Stance (4)", "Pre-Swing (5)", "Initial Swing (6)", "Midswing (7)", "Terminal swing (8)"], state='readonly', width=20)
        self.leg_phase_scroll.set("Initial Contact (1)")  # Set initial value
        self.leg_phase_scroll.pack(side=tk.LEFT, padx=10)
        self.leg_phase_scroll.bind("<<ComboboxSelected>>", self.update_labels)

        # Send to database
        self.refresh_button_frame = ttk.Frame(self.patientTable_frame, borderwidth=0, bootstyle="light")
        self.refresh_button_frame.grid(row=1, column=1, sticky="e", pady=(20, 20))

        # Refresh button
        self.refresh_button = ttk.Button(self.refresh_button_frame, width=10, text="Refresh", cursor="hand2", takefocus=False,
                                         style='search.TButton', command=self.refresh_data)
        self.refresh_button.pack(side=tk.RIGHT, padx=20)

        # Create a frame to hold the labels
        self.labels_frame = tk.Frame(self.patientTable_frame, padx=20, pady=20)
        self.labels_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")  # Span both columns

        self.update_labels()  # Initial population of labels

        # Configure window size and center on parent
        self.update_idletasks()  # Update the window to calculate frame size
        #width = self.labels_frame.winfo_reqwidth()  # Add padding
        #height = self.labels_frame.winfo_reqheight() # Add padding
        #x = (self.winfo_screenwidth() - width) // 2
        #y = (self.winfo_screenheight() - height) // 2
        #self.geometry(f"{width}x{height}+{x}+{y}")

    def update_labels(self, event=None):
        leg = self.leg_scroll.get()
        assessment_num = self.assessment_num
        
        # Get the selected phase string from the combobox
        selected_phase = self.leg_phase_scroll.get()

        # Extract the phase number using regular expressions
        phase_number_match = re.search(r'\d+', selected_phase)

        # Check if a number is found
        if phase_number_match:
            # Extract the phase number as an integer
            phase = int(phase_number_match.group())
        else:
            # Handle the case when no number is found (default to 1)
            phase = 1 

        try:
                    # Connect to the database
                    conn = mysql.connector.connect(
                        host = "localhost",
	                user= "gaitrpi",
	                password = "gait123",
	                database="gaitdata"
                    )
                    cursor = conn.cursor()

                    # Query to fetch assessment details based on selected leg, gait phase, and assessment number
                    query = f"SELECT a.image, a.frame," \
                            f" a.hips, a.knees, a.ankle, a.insole " \
                            f"FROM patient_info pd " \
                            f"INNER JOIN assessment a ON pd.client_id = a.client_id " \
                            f"WHERE a.side = '{leg}' AND a.phase = {phase} AND a.assessment_num = {assessment_num} AND a.client_id = {self.client_id} AND a.date_time = '{self.date}'"
                    cursor.execute(query)
                    data = cursor.fetchall()

                    # Clear previous labels
                    for widget in self.labels_frame.winfo_children():
                        widget.destroy()

                    # Create a canvas widget
                    canvas = tk.Canvas(self.labels_frame)
                    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx= 50, pady = 20)

                    # Create a scrollbar for the canvas
                    scrollbar = ttk.Scrollbar(self.labels_frame, orient=tk.VERTICAL, command=canvas.yview)
                    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    canvas.configure(yscrollcommand=scrollbar.set)

                    # Create a frame to hold the labels inside the canvas
                    inner_frame = tk.Frame(canvas)
                    canvas.create_window((0, 0), window=inner_frame, anchor='nw')

                    # Define headlines and corresponding column indexes
                    headlines = ["Image","Frame", "Hips", "Knees", "Ankle", "Insole"]
                    column_indexes = [0, 1, 2, 3, 4, 5]

                    # Display headlines
                    for col, headline in zip(column_indexes, headlines):
                        headline_label = tk.Label(inner_frame, text=headline, font=("montserrat", 14, "bold"))
                        headline_label.grid(row=0, column=col, padx=20, pady=10)

                    # Display assessment details for each row of data
                    for row_num, row_data in enumerate(data, start=1):
                        for col, value in zip(column_indexes, row_data):
                            if col == 0 and value:  # Check if column is 'Image' and value is not None
                                image_file_path = f"{value}"  # Use 'value' directly for image path

                                try:
                                    # Load and resize image using PIL
                                    image_pil = Image.open(image_file_path)
                                    image_resized = image_pil.resize((175, 175))
                                    image_tk = ImageTk.PhotoImage(image_resized)
                                    # Create a label to display the image
                                    image_label = tk.Label(inner_frame, image=image_tk)
                                    image_label.image = image_tk  # Keep reference to the image to prevent garbage collection
                                    image_label.grid(row=row_num, column=col, padx=10, pady=5)
                                except Exception as e:
                                    print(f"Error loading image: {e}")
                            else:
                                # Create text label for other columns
                                detail_label = tk.Label(inner_frame, text=value, anchor="w", justify="left", wraplength=200, font=("montserrat", 12))
                                detail_label.grid(row=row_num, column=col, padx=10, pady=5)
                                
                                #TODO - Change text color to red if true, dunno how to change color
                                if col == 2: #hip
                                    text = value.replace("°","")
                                    angle,rom = text.split(" ")
                                    print(rom)
                                    print(angle)
                                    if rom == "Extension":		
                                        if float(angle) > 25:
                                            #change text color to red
                                            detail_label.configure(fg = 'red')
                                            print('true')
                                    elif rom == "Flexion":		
                                        if float(angle) >25:
                                            #change text color to red
                                            detail_label.configure(fg = 'red')
                                            print('true')	
                                if col == 3:#knee
                                    text = value.replace("°","")
                                    angle,rom = text.split(" ")
                                    if rom == "Extension":		
                                        if float(angle) >5:
                                            #change text color to red
                                            detail_label.configure(fg = 'red')
                                            print('true')
                                    elif rom == "Flexion":		
                                        if float(angle) >65:
                                            #change text color to red
                                            detail_label.configure(fg = 'red')
                                            print('true')
                                if col == 4:#ankle
                                    text = value.replace("°","")
                                    angle,rom = text.split(" ")
                                    if rom == "Dorsiflexion":		
                                        if float(angle) >10:
                                            #change text color to red
                                            detail_label.configure(fg = 'red')
                                            print('true')
                                    elif rom == "Plantarflexion":		
                                        if float(angle) >25:
                                            #change text color to red
                                            detail_label.configure(fg = 'red')
                                            print('true')	
                                if col == 5 and value:  # Check if column is 'Image' and value is not None
                                    image_file_path2 = f'Data Inputs/insole_rep/{leg}/{value}.jpg'  # Use 'value' directly for image path

                                    try:
                                        # Load and resize image using PIL
                                        image_pil = Image.open(image_file_path2)
                                        image_resized = image_pil.resize((175, 175))
                                        image_tk = ImageTk.PhotoImage(image_resized)
                                        # Create a label to display the image
                                        image_label = tk.Label(inner_frame, image=image_tk)
                                        image_label.image = image_tk  # Keep reference to the image to prevent garbage collection
                                        image_label.grid(row=row_num, column=col, padx=10, pady=5)
                                    except Exception as e:
                                        print(f"Error loading image: {e}")
                            

                    # Update the scroll region of the canvas
                    inner_frame.update_idletasks()
                    canvas.configure(scrollregion=canvas.bbox("all"))

                    cursor.close()
                    conn.close()

        except mysql.connector.Error as e:
                    print(f"Error retrieving data from database: {e}")
        pass

    def refresh_data(self):
        self.update_labels()

class Process_Table(ttk.Frame):
    def __init__(self, parent, style):
        super().__init__(parent)

        self.style = style

        self.left_model = None
        self.right_model = None
        self.phase_frames = []
        

        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

        self.side_frame_numbers = {'Left': {}, 'Right': {}}
        self.angles_dict = {'Right': {}, 'Left': {}}
        print(f"Left: {self.master.side_state['Left']}")
        print(f"Right: {self.master.side_state['Right']}")

        self.loading_screen = ttk.Frame(self)
        self.loading_screen.pack(fill='both', expand=True)

        self.percent_label = ttk.Label(self.loading_screen, text="", anchor='center', justify='center', font=('Montserrat', 20))
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
                # If it's a file, remove it
                os.remove(item_path)

    def calculate_angle_hip(self, side, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        new_angle = 180 - angle
        if side == "Right":
            if new_angle < 0:
                final_angle = f"{round(abs(new_angle), 2)} Extension"
            else:
                final_angle = f"{round(abs(new_angle), 2)} Flexion"
        else:
            if new_angle < 0:
                final_angle = f"{round(abs(new_angle), 2)} Flexion"
            else:
                final_angle = f"{round(abs(new_angle), 2)} Extension"

        return final_angle

    def calculate_angle_knee(self, side, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        new_angle = 180 - angle

        if side == "Right":
            if new_angle < 0:
                final_angle = f"{round(abs(new_angle), 2)} Flexion"
            else:
                final_angle = f"{round(abs(new_angle), 2)} Extension"
        else:
            if new_angle < 0:
                final_angle = f"{round(abs(new_angle), 2)} Extension"
            else:
                final_angle = f"{round(abs(new_angle), 2)} Flexion"

        return final_angle

    def calculate_angle_ankle(self, side, a, b, c):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)

        if side == "Right":
            new_angle = 90 - angle
        else:
            new_angle = 90 - (360 - angle)
        
        if new_angle < 0:
            if abs(new_angle) > 40:
                new_angle += 40
            elif abs(new_angle) > 30:
                new_angle += 30
            elif abs(new_angle) > 20:
                new_angle += 20
            elif abs(new_angle) > 10:
                new_angle += 10
            final_angle = f"{round(abs(new_angle), 2)} Plantarflexion"
        else:

            if abs(new_angle) > 40:
                new_angle -= 40
            elif abs(new_angle) > 30:
                new_angle -= 30
            elif abs(new_angle) > 20:
                new_angle -= 20
            elif abs(new_angle) > 10:
                new_angle -= 10
            final_angle = f"{round(abs(new_angle), 2)} Dorsiflexion"

        return final_angle
        
    def crop_vid(self, side, folder_path):
        output_folder = f'Data_process/{side}'
        os.makedirs(output_folder, exist_ok=True)
        
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        file_list = sorted([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name)) and name.endswith('.jpg')])
        total_items = len(file_list)
                
        for i, files in enumerate(file_list):
            if files.endswith('.jpg'):
                frame_path = os.path.join(folder_path, files)
                frame_number = int(os.path.splitext(files)[0])

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

                    if side == "Right":
                        # Right Side Landmarks Indices
                        hip = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y])
                        knee = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y])
                        ankle = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y])
                        shoulder = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y])
                        foot_index = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y])
                        heel = np.array([landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y])
                        
                    else:
                        # Left Side Landmarks Indices
                        hip = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y])
                        knee = np.array([landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y])
                        ankle = np.array([landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y])
                        shoulder = np.array([landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y])
                        foot_index = np.array([landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y])
                        heel = np.array([landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y])
                        
                    
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
                            
                            # Calculate the midpoint between foot_index and heel, 70% closer to heel
                            new_landmark = heel - 0.2 * (heel - foot_index)
                            
                            # Calculate angles
                            hip_angle = self.calculate_angle_hip(side, shoulder, hip, knee)
                            knee_angle = self.calculate_angle_knee(side, hip, knee, ankle)
                            ankle_angle = self.calculate_angle_ankle(side, ankle, new_landmark, foot_index)
                            
                            self.angles_dict[side][frame_number] = {'hip': f"{hip_angle}", 'knee': f"{knee_angle}", 'ankle': f"{ankle_angle}"}
                    progress_percent = int(round((i/total_items), 2) * 100)
                    if progress_percent> 100:   
                        progress_percent = 100
                    self.percent_label.config(text=f"{side} side, currently processing: {progress_percent}%")


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

        #create a main frame
        self.main_assessment_frame = ttk.Frame(self, borderwidth= 0, bootstyle = 'light')
        self.main_assessment_frame.grid(row = 0, column= 0, padx = 20, pady = 20, sticky= 'nsew')

        self.main_assessment_frame.grid_columnconfigure(0, weight = 1)
        self.main_assessment_frame.grid_rowconfigure(6, weight = 5)

        self.title_Assessment = ttk.Label(self.main_assessment_frame, text= "Gait Assessment Table", font= ('raleway', 18, 'bold'), bootstyle = 'inverse-light')
        self.title_Assessment.grid(row = 0, column = 0, pady = (20, 20))

        self.current_Patient = ttk.Label(self.main_assessment_frame, text= f'Current Patient: {self.master.current_patient_id}', font= ('montserrat', 12, 'bold'), bootstyle = 'inverse-light')
        self.current_Patient.grid(row = 1, column = 0 ,pady = (0, 20))

        #add a frame for tools
        self.tool_frame_2 = ttk.Frame(self.main_assessment_frame, borderwidth= 0, bootstyle = "light")
        self.tool_frame_2.grid(row = 2 , column = 0, sticky="ew", pady = (20, 20))
        
        if self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 0:
            # Create a Combobox to select the side (Left or Right)
            self.side_var = tk.StringVar()
            self.side_var.set('Right')  # Default value
            self.side_selector = ttk.Combobox(self.tool_frame_2, textvariable=self.side_var, values=['Right'], state="readonly", width= 15)

        elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:
            # Create a Combobox to select the side (Left or Right)
            self.side_var = tk.StringVar()
            self.side_var.set('Left')  # Default value
            self.side_selector = ttk.Combobox(self.tool_frame_2, textvariable=self.side_var, values=['Left'], state="readonly",width= 15)
        else:
            # Create a Combobox to select the side (Left or Right)
            self.side_var = tk.StringVar()
            self.side_var.set('Left')  # Default value
            self.side_selector = ttk.Combobox(self.tool_frame_2, textvariable=self.side_var, values=['Left', 'Right'], state="readonly", width= 15)
        
        #label
        self.side_selector_label = ttk.Label(self.tool_frame_2, text = "Current Leg: ", font=('raleway', 12, 'bold'), bootstyle = 'inverse-light')
        self.side_selector_label.pack(side= tk.LEFT, padx = (20, 10))
        self.side_selector.pack(side= tk.LEFT, padx = (10, 20))
        
        self.side_label = ttk.Label(self.tool_frame_2, text="Gait Phase:", font=('raleway', 12, 'bold'), bootstyle = 'inverse-light')
        self.side_label.pack(side= tk.LEFT, padx = (20, 10))
        
        self.phase_selector = ttk.Combobox(self.tool_frame_2, values=["Initial Contact (1)", "Loading Response (2)", "Midstance (3)", "Terminal Stance (4)", "Pre-Swing (5)", "Initial Swing (6)", "Midswing (7)", "Terminal swing (8)"], state='readonly', width=18)
        self.phase_selector.set("Initial Contact (1)")  # Set initial value
        self.phase_selector.pack(side= tk.LEFT, padx = (20, 10))
        
        #label
        #self.side_label = ttk.Label(self.tool_frame_2, text = "Gait Phase: ", font=('raleway', 14, 'bold'), bootstyle = 'inverse-light')
        #self.side_label.pack(side= tk.LEFT, padx = (20, 10))

        # Create a Combobox to select phase number
        #self.phase_number_var = tk.StringVar()
        #self.phase_number_var.set('1')  # Default value
        #self.phase_selector = ttk.Combobox(self.tool_frame_2, textvariable=self.phase_number_var, values=[str(i) for i in range(1, 9)], state="readonly")
        #self.phase_selector.pack(side= tk.LEFT, padx = (20, 10))

        # Button to populate the table
        self.populate_button = ttk.Button(self.tool_frame_2, text="Populate Table", bootstyle = 'primary', style='main.TButton'
                                          , takefocus= False, cursor = 'hand2', 
                                          command = self.update_table) #add command to populate table
        self.populate_button.pack(side= tk.RIGHT, padx = (20, 10))

        # Button to send data
        self.send_button = ttk.Button(self.tool_frame_2, text="Save", bootstyle = 'primary', style='main.TButton'
                                          , takefocus= False, cursor = 'hand2', 
                                          command = self.send_data) #add command to send data
        self.send_button.pack(side= tk.RIGHT, padx = (0, 10))
        
        # Go-back to menu_bar
        self.end_button = ttk.Button(self.tool_frame_2, text="Exit", bootstyle = 'danger', style='danger.TButton'
                                          , takefocus= False, cursor = 'hand2', 
                                          command = lambda: self.master.change_frame(self, MenuBar))
        self.end_button.pack(side= tk.RIGHT, padx = (10, 20))

        self.frame_canvas = ttk.Frame(self.main_assessment_frame, borderwidth= 0, bootstyle = 'light')
        self.frame_canvas.grid(row = 3, column= 0, padx = 10, pady = 10, sticky= 'nsew')

        self.frame_canvas.grid_columnconfigure(0, weight = 1)
        self.frame_canvas.grid_rowconfigure(0, weight = 1)

        # Create a canvas and attach a scrollbar to it
        self.canvas = tk.Canvas(self.frame_canvas, height= 400)
        self.canvas.grid(row=0, column=0, sticky='nsew', padx = 10, pady = 10)

        self.scrollbar = ttk.Scrollbar(self.frame_canvas, orient='vertical', command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # Configure the canvas to utilize the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame to contain all widgets
        self.scrollable_frame = tk.Frame(self.canvas)
        
        self.scrollable_frame.grid_columnconfigure(0, weight = 1)
        self.scrollable_frame.grid_rowconfigure(0, weight = 1)
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw', width= 1200)

        # Update scroll region when the size of the frame changes
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Make the canvas scrollable with the mouse wheel
        self.canvas.bind('<MouseWheel>', lambda event: self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

        # Create a frame for the table-like structure
        self.table_frame = tk.Frame(self.scrollable_frame)
        
        self.table_frame.grid_columnconfigure(0, weight = 2)
        self.table_frame.grid_columnconfigure(1, weight = 2)
        self.table_frame.grid_columnconfigure(2, weight = 3)
        self.table_frame.grid_columnconfigure(3, weight = 3)
        self.table_frame.grid_columnconfigure(4, weight = 3)
        self.table_frame.grid_columnconfigure(5, weight = 2)
        
        self.table_frame.grid(row=0, column=0, sticky='nsew', padx = 60, pady= 20)
        
        # Define headings
        headings = ['Frame Image', 'Frame Num', 'ROM Hips', 'ROM Knees', 'ROM Ankle', 'Insole']

        # Create labels for headings with font size 20
        for col, heading in enumerate(headings):
            heading_label = tk.Label(self.table_frame, text=heading, font=('raleway', 14, 'bold'),
                                     borderwidth=1, relief='solid')
            heading_label.grid(row=0, column=col, sticky="nsew")
        
        
    def send_data(self): #run ONLY ONCE
        conn = mysql.connector.connect(
        host = "localhost",
	    user= "gaitrpi",
        password = "gait123",
	    database="gaitdata"
        )

        mycursor = conn.cursor(buffered=True)
        client_id = self.master.current_patient_id
        #DONE: get date, and determine if an assessment is performed before this one, if no assessment performed on date, set assessment value as 1, RUN ONCE
        date = datetime.today().strftime('%Y-%m-%d')
        #date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        #print(date)
        sql = "SELECT assessment_num from assessment WHERE date_time=%s ORDER BY assessment_num DESC" #get the highest assessment number 
        val = (date,)
        mycursor.execute(sql,val)
        result = mycursor.fetchone()
        if result is not None:
            assessment_num = result[0] + 1
        else:
            assessment_num = 1
        
        #DONE: move img from data_process to Database folder, directory is as follows, RUN ONCE
        #DIR: Database/client_id/date(YYYYMMDD)/assessment_num/(Left/Right)/frame_num.jpg
        target_path = f"Database/{client_id}/{date}/{assessment_num}"
        #PS: IF directory specified does not exists, create dir
        
        #DONE: forloop this shit
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
        conn.commit()
        print(f"sent {count} data")
        messagebox.showinfo(f"Sent data", "Data Saved")
        self.master.change_frame(self, MenuBar)

    def load_model_for_side(self, side):
        return load_model(f'Data Inputs/models/{side}_official.h5')
    
    def find_nearest(input,reference_list):
        return min(reference_list,key=lambda d: abs(d - input))
        
    def process_images_for_side(self, side, model):
        test_data_dir = f'Data_process/{side}'
        image_files = sorted(os.listdir(test_data_dir))  # Sort the files for consistency
        
        # Exclude the first 10 and last 10 frames
        #image_files = image_files[5:-5]
        insole = 'temp'
        if side == 'Left' and self.master.synced_left:
            synced_frame,synced_insole = map(list,zip(*self.master.synced_left))#format is (frame,insole)
        elif side == 'Right' and self.master.synced_right:
            synced_frame,synced_insole = map(list,zip(*self.master.synced_right))#format is (frame,insole)
        else:
            insole = "unknown"
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
                rom_h = self.try_me(side,frame_num,'hip')
                rom_k = self.try_me(side,frame_num,'knee')
                rom_a = self.try_me(side,frame_num,'ankle')
                if self.master.synced_left and side =="Left" or side == "Right" and self.master.synced_right:
                    #find index of synced list to match current frame
                    synced_index = synced_frame.index(frame_num)
                    #get insole data from index
                    insole = synced_insole[synced_index]
                
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
                if current_percent > 100:
                    current_percent = 100
                self.percent_label.config(text=f"{side} side, analyzing and classifying data: {current_percent}%")
    def try_me(self,side,frame_num,joint):
        try:
            angle = self.angles_dict[side][frame_num][joint]
        except KeyError:
            angle = 'Unknown'
        return angle
    
    def update_table(self):
        current_side = self.side_var.get()
        phase_number = self.phase_selector.get()

        # Extract the phase number using regular expressions
        phase_number_match = re.search(r'\d+', phase_number)

        # Check if a number is found
        if phase_number_match:
            # Extract the phase number as an integer
            phase = int(phase_number_match.group())
        else:
            # Handle the case when no number is found (default to 1)
            phase = 1 

        if current_side == 'Left':
            self.populate_table_frame(self.table_frame, "Left", phase)
        else:
            self.populate_table_frame(self.table_frame, "Right", phase)
    
    def populate_table_frame(self, table_frame, select_side, phase_number):
        # Clear existing widgets from table_frame
        
        for widget in table_frame.winfo_children():
            if widget.grid_info()['row'] != 0:
                widget.destroy()
        
        #filter dictionary
        filtered_dict = [d for d in self.phase_frames if d['side'] == select_side and d['phase'] == phase_number]
        for x in filtered_dict:
            print(x)
        #print(f"Filtered Data: {len(filtered_dict)} entries")
        
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
            img_label.grid(row=row+1, column=0, sticky="nsew", ipadx = 10, ipady = 10)

            # Display other information with font size 20
            self.frame_num = tk.Label(table_frame, text=frame_num, font=('montserrat', 14), borderwidth=1, relief='solid')
            self.frame_num.grid(row=row+1, column=1, sticky="nsew")
            self.rom_h = tk.Label(table_frame, text=rom_h, font=('montserrat', 14), borderwidth=1, relief='solid')#change text color if value exceeds 
            self.rom_h.grid(row=row+1, column=2, sticky="nsew") 
            self.rom_k = tk.Label(table_frame, text=rom_k, font=('montserrat', 14), borderwidth=1, relief='solid')
            self.rom_k.grid(row=row+1, column=3, sticky="nsew") #change text color if value exceeds
            self.rom_a = tk.Label(table_frame, text=rom_a, font=('montserrat', 14), borderwidth=1, relief='solid')
            self.rom_a.grid(row=row+1, column=4, sticky="nsew") #change text color if value exceeds
            #tk.Label(table_frame, text=insole, font=('montserrat', 20), borderwidth=1, relief='solid').grid(row=row+1, column=5, sticky="nsew")
            
            #TODO Change color to red
            text_hip = rom_h.replace("°","") #hip
            angle_hip,rom_hip = text_hip.split(" ")

            if rom_hip == "Extension":		
                if float(angle_hip) >25:
                    #change text color to red
                    self.rom_h.configure(fg = 'red')
                    print('true')
            elif rom_hip == "Flexion":		
                if float(angle_hip) >25:
                    #change text color to red
                    self.rom_h.configure(fg = 'red')
                    print('true')
                   	
            text_knee = rom_k.replace("°","")#knee
            angle_knee,rom_knee = text_knee.split(" ")
            
            if rom_knee == "Extension":		
                if float(angle_knee) > 5:
                    #change text color to red
                    self.rom_k.config(fg = 'red')
                    print('true')
            elif rom_knee == "Flexion":		
                if float(angle_knee) >65:
                    #change text color to red
                    self.rom_k.config(fg = 'red')
                    print('true')
                    
            text_ankle = rom_a.replace("°","")#ankle
            angle_ankle,rom_ankle = text_ankle.split(" ")
            
            if rom_ankle == "Dorsiflexion":		
                if float(angle_ankle) >10:
                    #change text color to red
                    self.rom_a.config(fg = 'red')
                    print('true')
            elif rom_ankle == "Plantarflexion":		
                if float(angle_ankle) >25:
                    #change text color to red
                    self.rom_a.config(fg = 'red')
                    print('true')
    
            # Display image
            img2 = Image.open(f'Data Inputs/insole_rep/{frame_info["side"]}/{insole}.jpg')
            img2.thumbnail((175, 175))  # Resize image if necessary
            img2 = ImageTk.PhotoImage(img2)
            img_label2 = tk.Label(table_frame, image=img2, borderwidth=1, relief='solid')
            img_label2.image = img2  # Keep reference to avoid garbage collection
            img_label2.grid(row=row+1, column=5, sticky="nsew")
        

if __name__ == "__main__":
    app = refApp((1280, 700))
    app.state('normal')
    app.attributes('-zoomed', True)  # change back to -zoomed if in rpi 
    app.mainloop()

