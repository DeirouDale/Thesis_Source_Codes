import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

#TODO: add a horizontal bar for extra data
#TODO: instead na isend data to db in this file, well just put it in a csv file and send it from there using the phpconnect.py file
def load_model_for_side(side):
    return load_model(f'Data_collection/models/{side}_10_Pat_New2.h5')

def process_images_for_side(side, model):
    test_data_dir = f'Data_process/{side}'
    image_files = os.listdir(test_data_dir)
    phase_frames = {phase_num: {} for phase_num in range(1, 9)}

    for image_file in image_files:
        if image_file.endswith('.jpg'):
            frame_num = int(os.path.splitext(image_file)[0])
            image_path = os.path.join(test_data_dir, image_file)
            img = cv2.imread(image_path)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            resize = cv2.resize(img_rgb, (256, 256))
            normalized_img = resize / 255.0
            yhat_single = model.predict(np.expand_dims(normalized_img, axis=0))
            predicted_class = int(np.argmax(yhat_single, axis=1))
            phase_frames[predicted_class + 1][frame_num] = {
                'frame_name': f'frame {frame_num}',
                'image_path': image_path,
                'rom_h': 'sample',
                'rom_k': 'sample',
                'rom_a': 'sample',
                'insole': 'sample',
            }
    return phase_frames

def populate_table_frame(table_frame, phase_frames, phase_number):
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


# Main Tkinter application
root = tk.Tk()
root.state('zoomed')

# Load models for Left and Right
left_model = load_model_for_side('Left')
right_model = load_model_for_side('Right')

# Process images for Left and Right
left_phase_frames = process_images_for_side('Left', left_model)
right_phase_frames = process_images_for_side('Right', right_model)

def populate_table():
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

    current_side = side_var.get()
    phase_number = int(phase_number_var.get())
    if current_side == 'Left':
        populate_table_frame(table_frame, left_phase_frames, phase_number)
    else:
        populate_table_frame(table_frame, right_phase_frames, phase_number)

# Create a Combobox to select the side (Left or Right)
side_var = tk.StringVar()
side_var.set('Left')  # Default value
side_selector = ttk.Combobox(root, textvariable=side_var, values=['Left', 'Right'], state="readonly")
side_selector.pack()

# Create a Combobox to select phase number
phase_number_var = tk.StringVar()
phase_number_var.set('1')  # Default value
phase_selector = ttk.Combobox(root, textvariable=phase_number_var, values=[str(i) for i in range(1, 9)], state="readonly")
phase_selector.pack()


# Button to populate the table
populate_button = tk.Button(root, text="Populate Table", command=populate_table)
populate_button.pack()

# Create a canvas and attach a scrollbar to it
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill='both', expand=True)

scrollbar = ttk.Scrollbar(root, orient='vertical', command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill='y')

# Configure the canvas to utilize the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame to contain all widgets
scrollable_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor='center', width=1920)

# Update scroll region when the size of the frame changes
scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Make the canvas scrollable with the mouse wheel
canvas.bind('<MouseWheel>', lambda event: canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

# Create a frame for the table-like structure
table_frame = tk.Frame(scrollable_frame)
table_frame.pack()

root.mainloop()
