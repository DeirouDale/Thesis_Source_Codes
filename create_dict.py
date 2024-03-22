import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Define class names
class_names = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5', 'Phase 6', 'Phase 7', 'Phase 8']

side = 'Right'

# Load your pre-trained model
new_model = load_model(f'Data_collection/models/{side}_10_Pat_New2.h5')

test_data_dir = f'Data_process/{side}'

image_files = os.listdir(test_data_dir)

# Create an empty dictionary to store frame numbers for Phase 1, along with their frame names and images
phase1_frames = {}

for image_file in image_files:
    if image_file.endswith('.jpg') and image_file.startswith('frame_'):
        frame_num = int(image_file.split('_')[1].split('.')[0])  # Extract frame number from the image file name

        image_path = os.path.join(test_data_dir, image_file)

        img = cv2.imread(image_path)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        resize = cv2.resize(img_rgb, (256, 256))

        normalized_img = resize / 255.0

        yhat_single = new_model.predict(np.expand_dims(normalized_img, axis=0))

        predicted_class = int(np.argmax(yhat_single, axis=1))

        # Check if the predicted class is Phase 1 (class index 0)
        if predicted_class == 0:
            # Add the frame number and its corresponding frame name and image to the dictionary
            phase1_frames[frame_num] = {'frame_name': f'frame {frame_num}', 'image_path': image_path}

# Now, phase1_frames dictionary contains frame numbers as keys,
# and each value is a dictionary containing the frame name and its corresponding image path


def show_image(image_path):
    # Open the image file
    image = Image.open(image_path)
    # Resize image for display
    image = image.resize((250, 250))
    # Convert Image object to Tkinter PhotoImage object
    photo = ImageTk.PhotoImage(image)
    
    return photo


def populate_table(data, parent):
    for frame_num, frame_data in data.items():
        frame_name = frame_data['frame_name']
        image_path = frame_data['image_path']
        # Load image and convert to Tkinter PhotoImage
        photo = show_image(image_path)
        # Create label to display the image
        label = tk.Label(parent, image=photo)
        label.photo = photo  # Keep reference to prevent garbage collection
        label.pack()
        # Create label to display frame name
        ttk.Label(parent, text=frame_name).pack()


# Create tkinter window
root = tk.Tk()
root.title("Phase 1 Table")
root.geometry("800x800")

# Create a frame for the canvas and scrollbar
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Create canvas
canvas = tk.Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add scrollbar
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure canvas
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create another frame inside canvas
scrollable_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Populate the table with phase1_frames data
populate_table(phase1_frames, scrollable_frame)

# Run the tkinter event loop
root.mainloop()
