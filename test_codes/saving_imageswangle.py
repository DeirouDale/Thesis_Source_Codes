import cv2
import mediapipe as mp
import os
import numpy as np
import math  # Add this line to import the math module
from PIL import Image

vid_name = 'vid5'
# Path to the video file
video_path = f'Data_collection/videos/{vid_name}.mp4'

# Path to the folder where frames with landmarks will be saved
output_folder = 'MP_Frames'
os.makedirs(output_folder, exist_ok=True)

# Initialize MediaPipe Pose model
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.8, min_tracking_confidence=0.8)

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

    # Check if landmarks are detected
    if results.pose_landmarks:
        # Draw landmarks on the frame
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get landmarks
        landmarks = results.pose_landmarks.landmark

        # Extract specific landmarks
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        left_foot_tip = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        right_foot_tip = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

        # Set bounding box coordinates
        if left_hip and left_ankle and left_foot_tip and right_hip and right_ankle and right_foot_tip:
            x_min = int(min(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1]) - 70
            y_min = int(min(left_hip.y, right_hip.y) * frame.shape[0]) - 70
            x_max = int(max(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1]) + 70
            y_max = int(max(left_ankle.y, right_ankle.y, left_foot_tip.y, right_foot_tip.y) * frame.shape[0]) + 60

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

                #imgWhite = cv2.cvtColor(imgWhite, cv2.COLOR_BGR2RGB)

                # Save the frame with landmarks and bounding box to the output folder
                file_name = f"{vid_name}_{frame_number}.jpg"
                file_path = os.path.join(output_folder, file_name)
                cv2.imwrite(file_path, imgWhite)
                print(f"Landmarks detected in frame {frame_number}.")

    else:
        print(f"No landmarks detected in frame {frame_number}.")

# Release the video capture object
cap.release()
cv2.destroyAllWindows()
