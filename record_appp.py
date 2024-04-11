import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import math 
import threading

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
        self.side_state = {'Right': 0, 'Left':0}

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
                end_btn = ttk.Button(self.choose_side_btn2, text="End Video Taking", command=lambda: self.master.change_frame(self, Title))

                side_btn.grid(row=0, column=0, sticky='nsew')
                end_btn.grid(row=0, column=1, sticky='nsew')
            elif self.master.side_state['Right'] == 0 and self.master.side_state['Left'] == 1:
                self.choose_side_btn2 = ttk.Frame(self)
                self.choose_side_btn2.grid(row=2, column=0, sticky='nsew')

                self.choose_side_btn2.columnconfigure((0,1), weight=1)
                self.choose_side_btn2.rowconfigure(0, weight=1)

                side_btn = ttk.Button(self.choose_side_btn2, text=f"Start Right Side", command=lambda: self.change_button('right'))
                end_btn = ttk.Button(self.choose_side_btn2, text="End Video Taking", command=lambda: self.master.change_frame(self, Title))

                side_btn.grid(row=0, column=0, sticky='nsew')
                end_btn.grid(row=0, column=1, sticky='nsew')
            elif self.master.side_state['Right'] == 1 and self.master.side_state['Left'] == 1:
                self.master.change_frame(self, Title)
        
    def toggle_recording(self, state):
        if not self.recording:
            self.recording = True
            self.record_button.config(text="Stop Recording")
            
            if state == 1 or state == 6:
                self.assessment_state_text = 'Left'
            elif state == 2 or state == 7:
                self.assessment_state_text = 'Right'
            
            self.output_filename = f'Data_process/{self.assessment_state_text}_vid.avi'
            self.out = cv2.VideoWriter(self.output_filename, self.fourcc, 10.0, (1280, 720))
            
        else:
            self.recording = False
            self.record_button.config(text="Start Recording")
            self.out.release()
            self.change_button('choose_other')
            
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


if __name__ == "__main__":
    app = RefApp((1920, 1080))
    app.state('zoomed')
    app.mainloop()
