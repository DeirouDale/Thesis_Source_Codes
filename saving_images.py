import cv2
import mediapipe as mp
import os
import numpy as np
import math 

# Path to the video file
vid_name = 'vid2'
video_path = f'Data_collection/videos/{vid_name}.mp4'

# Path to the folder where frames with landmarks will be saved
output_folder = 'Frames'
os.makedirs(output_folder, exist_ok=True)

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file is opened successfully
if not cap.isOpened():
    print("Error: Could not open the video file.")
    exit()

# Get the total number of frames in the video
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Iterate through each frame
for frame_number in range(1, total_frames + 1):
    # Set the frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)  # Frame numbering starts from 0

    # Read the frame
    ret, frame = cap.read()

    # Check if the frame is read successfully
    if not ret:
        print(f"Error: Could not read frame {frame_number}.")
        break

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect landmarks
    results = pose.process(frame_rgb)

    # Check if landmarks are found
    if results.pose_landmarks:
        # Define landmarks to display (indices 23 to 32)
        landmarks_to_show = [23, 24, 25, 26, 27, 28, 29, 30, 31, 32]

        # Draw landmarks for specified landmarks if they are within the visible screen
        for landmark in landmarks_to_show:
            landmark_pos = results.pose_landmarks.landmark[landmark]
            # Convert landmark position to pixel coordinates
            height, width, _ = frame.shape
            cx, cy = int(landmark_pos.x * width), int(landmark_pos.y * height)
            # Draw the landmark on the frame if it is within the visible screen
            if 0 <= cx < width and 0 <= cy < height:
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        # Define connections between landmarks
        connections = [
            [(23, 25), (25, 27), (27, 31), (31, 29), (29, 27)],
            [(24, 26), (26, 28), (28, 32), (32, 30), (30, 28)],
            [(23, 24)]
        ]

        # Define colors for connections
        colors = [(255, 0, 0), (0, 0, 255), (255, 255, 255)]

        # Initialize bounding box coordinates
        x_min = width
        y_min = height
        x_max = 0
        y_max = 0

        # Iterate through connections to find bounding box coordinates and draw connections
        for connection_set, color in zip(connections, colors):
            for connection in connection_set:
                start_landmark = connection[0]
                end_landmark = connection[1]
                start_pos = results.pose_landmarks.landmark[start_landmark]
                end_pos = results.pose_landmarks.landmark[end_landmark]
                start_x, start_y = int(start_pos.x * width), int(start_pos.y * height)
                end_x, end_y = int(end_pos.x * width), int(end_pos.y * height)

                # Update bounding box coordinates
                x_min = min(x_min, min(start_x, end_x))
                y_min = min(y_min, min(start_y, end_y))
                x_max = max(x_max, max(start_x, end_x))
                y_max = max(y_max, max(start_y, end_y))

                # Draw connection lines
                cv2.line(frame, (start_x, start_y), (end_x, end_y), color, 3)

        # Expand bounding box with an offset of 50
        x_min = max(0, x_min - 50)
        y_min = max(0, y_min - 50)
        x_max = min(width, x_max + 50)
        y_max = min(height, y_max + 50)

        # Get the bounding box content
        bounding_box_content = frame[y_min:y_max, x_min:x_max]

        # Create a white image
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
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = 500 / content_width
                hCal = math.ceil(k * content_height)
                imgResize = cv2.resize(bounding_box_content, (500, hCal))
                hGap = math.ceil((500 - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            # Save the frame with landmarks and bounding box to the output folder
            file_name = f"{vid_name}_{frame_number}.jpg"
            file_path = os.path.join(output_folder, file_name)
            cv2.imwrite(file_path, imgWhite)
            print(f"Frame {frame_number} processed and saved with landmarks.")

    else:
        print(f"No landmarks detected in frame {frame_number}.")

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
