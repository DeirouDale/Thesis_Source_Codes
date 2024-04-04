import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Define class names
class_names = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5', 'Phase 6', 'Phase 7', 'Phase 8']

# Load your pre-trained model
def load_model_for_side(side):
    return load_model(f'Data_collection/models/{side}_10_Pat_New2.h5')

def process_images_for_side(side, model):
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
            phase_frames[predicted_class + 1][frame_num] = {
                'frame_name': f'frame {frame_num}',
                'image_path': image_path,
                'phase': predicted_class
                }

    return phase_frames

def show_image(image_path):
    # Open the image file
    image = Image.open(image_path)
    # Resize image for display
    image = image.resize((200, 200))
    # Convert Image object to Tkinter PhotoImage object
    photo = ImageTk.PhotoImage(image)
    
    return photo

def populate_table(data, parent):
    # Create labels for each phase
    ttk.Label(parent, text="Phase 1").grid(row=0, column=0, padx=10)
    ttk.Label(parent, text="Phase 2").grid(row=0, column=1, padx=10)
    ttk.Label(parent, text="Phase 3").grid(row=0, column=2, padx=10)
    ttk.Label(parent, text="Phase 4").grid(row=0, column=3, padx=10)
    ttk.Label(parent, text="Phase 5").grid(row=0, column=4, padx=10)
    ttk.Label(parent, text="Phase 6").grid(row=0, column=5, padx=10)
    ttk.Label(parent, text="Phase 7").grid(row=0, column=6, padx=10)
    ttk.Label(parent, text="Phase 8").grid(row=0, column=7, padx=10)

    # Initialize counters for each phase
    phase_counters = {phase_num: 1 for phase_num in range(1, 9)}

    # Populate the table with frames for each phase
    for phase_num, phase_data in data.items():
        for frame_num, frame_data in phase_data.items():
            frame_name = frame_data['frame_name']
            image_path = frame_data['image_path']
            # Load image and convert to Tkinter PhotoImage
            photo = show_image(image_path)
            # Create label to display the image
            label = tk.Label(parent, image=photo, borderwidth=1, relief="solid")
            label.photo = photo  # Keep reference to prevent garbage collection
            label.grid(row=phase_counters[phase_num], column=phase_num - 1, padx=10, pady=10)
            # Create label to display frame name
            ttk.Label(parent, text=frame_name, borderwidth=1, relief="solid").grid(row=phase_counters[phase_num] + 1, column=phase_num - 1, padx=10)
            # Increment counter for the current phase
            phase_counters[phase_num] += 2  # Increment by 2 to leave space for frame name

# Create tkinter window
root = tk.Tk()
root.title("Phase Tables")

# Maximize the window
root.state('zoomed')  # This maximizes the window

# Load models for Left and Right
left_model = load_model_for_side('Left')
right_model = load_model_for_side('Right')

# Process images for Left and Right
left_phase_frames = process_images_for_side('Left', left_model)
right_phase_frames = process_images_for_side('Right', right_model)

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
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas for the table
canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a scrollbar to the canvas
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure canvas scrolling
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside the canvas to hold the table
table_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=table_frame, anchor="nw")

# Populate the combined table
populate_table(combined_phase_frames, table_frame)

# Run the tkinter event loop
root.mainloop()
