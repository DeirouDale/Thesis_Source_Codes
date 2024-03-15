import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model

# Define class names
class_names = ['Phase 1', 'Phase 2', 'Phase 3', 'Phase 4', 'Phase 5', 'Phase 6', 'Phase 7', 'Phase 8']

side = 'Right'

phases = {name: [] for name in class_names}

# Load your pre-trained model
new_model = load_model(f'Data_collection/models/{side}_10_Pat_New2.h5')

# Directory containing test images
for i in range(1, 9):
    test_data_dir = f'test_data/{side}/Phase {i}'
    num_list = [0] * 8  # Initialize the list of counts for each phase
    
    # List all files in the directory
    image_files = os.listdir(test_data_dir)

    for image_file in image_files:
        # Construct the full path to the image file
        image_path = os.path.join(test_data_dir, image_file)
        
        # Read the image using OpenCV
        img = cv2.imread(image_path)
        
        # Convert BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize the image
        resize = cv2.resize(img_rgb, (256, 256))
        
        # Normalize the image
        normalized_img = resize / 255.0
        
        # Predict the class of the image
        yhat_single = new_model.predict(np.expand_dims(normalized_img, axis=0))
        predicted_class = int(np.argmax(yhat_single, axis=1))
        
        # Increment the count for the predicted class
        num_list[predicted_class] += 1

    # Assign the counts to the corresponding phase list
    phases[class_names[i-1]] = num_list

for phase_name, phase_values in phases.items():
    print(phase_name + ":", ' '.join(map(str, phase_values)))
