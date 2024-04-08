import cv2
import mediapipe as mp
import os
import numpy as np
import math
from PIL import Image
import csv

<<<<<<< HEAD
vid_name = 'vid 3'
=======
#TODO: Use this as reference for the application
# Function to calculate the angle between three points
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
    angle = round(angle, 2)
    return angle

angle_data = []
vid_name = 'vid4'
>>>>>>> 9601db50586704d57f73af88c7ea71e74ef22645
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
    print(f'Error: Could not open the Data_collection/videos/{vid_name}.mp4 file.')
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
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        left_foot_tip = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]
        right_foot_tip = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]
       
        angle_right_knee = calculate_angle([right_hip.x, right_hip.y], [right_knee.x, right_knee.y], [right_ankle.x, right_ankle.y])
        angle_right_hip = calculate_angle([right_shoulder.x, right_shoulder.y], [right_hip.x, right_hip.y], [right_knee.x, right_knee.y])
        angle_right_ankle = calculate_angle([right_knee.x, right_knee.y], [right_ankle.x, right_ankle.y], [right_foot_tip.x, right_foot_tip.y])

        angle_left_knee = calculate_angle([left_hip.x, left_hip.y], [left_knee.x, left_knee.y], [left_ankle.x, left_ankle.y])
        angle_left_hip = calculate_angle([left_shoulder.x, left_shoulder.y], [left_hip.x, left_hip.y], [left_knee.x, left_knee.y])
        angle_left_ankle = calculate_angle([left_knee.x, left_knee.y], [left_ankle.x, left_ankle.y], [left_foot_tip.x, left_foot_tip.y])

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

                # Save the frame with landmarks and bounding box to the output folder
                angle_data.append([frame_number,angle_right_knee, angle_right_hip, angle_right_ankle, angle_left_knee, angle_left_hip, angle_left_ankle])
                #file_name = f"{vid_name}_{frame_number}.jpg"
                #file_path = os.path.join(output_folder, file_name)
                #cv2.imwrite(file_path, imgWhite)
                print(f"Landmarks detected in frame {frame_number}.")

    else:
        print(f"No landmarks detected in frame {frame_number}.")
#can specify the directory to save the csv file if needed.
with open(f'{vid_name}_angles.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Frame Number", "Right Knee Angle", "Right Hip Angle", "Right Ankle Angle", "Left Knee Angle", "Left Hip Angle", "Left Ankle Angle"])
    writer.writerows(angle_data)
# Release the video capture object
cap.release()
cv2.destroyAllWindows()
