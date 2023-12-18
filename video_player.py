import cv2
import mediapipe as mp
import numpy as np
import math
import time
import tkinter as tk
import os
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("Video Player")
        self.max_height = 800  # Maximum height of the video player

        self.video_path = video_path

        self.prev_time = 0
        self.frame_number = 0

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        self.drawing_bbox = False

        self.cap = cv2.VideoCapture(self.video_path)
        self.paused = False
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.video_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.video_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.imgSize = 500
        self.x_min, self.x_max = 0, 0
        self.y_min, self.y_max = 0, 0

        if self.video_height > self.max_height:
            self.video_width = int(self.video_width * (self.max_height / self.video_height))
            self.video_height = self.max_height

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=self.video_width, height=self.video_height)
        self.canvas.pack()

        self.btn_play = tk.Button(self.root, text="Play/Pause", command=self.play_pause)
        self.btn_play.pack(side=tk.LEFT)

        self.btn_save = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.btn_save.pack(side=tk.LEFT)

        self.scale = tk.Scale(self.root, from_=0, to=self.total_frames, orient=tk.HORIZONTAL)
        self.scale.pack(fill=tk.X)

        self.scale.bind("<ButtonRelease-1>", self.set_position)  # Update on slider release

        self.update()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.frame = frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.video_width, self.video_height))

            curr_time = time.time()
            if hasattr(self, 'prev_time'):
                fps = 1 / (curr_time - self.prev_time)
                self.prev_time = curr_time
            else:
                fps = 0
                self.prev_time = curr_time
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(frame_rgb)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark

                left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value]
                left_ankle = landmarks[self.mp_pose.PoseLandmark.LEFT_ANKLE.value]
                left_foot_tip = landmarks[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value]

                right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value]
                right_ankle = landmarks[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value]
                right_foot_tip = landmarks[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value]

                if left_hip and left_ankle and left_foot_tip and right_hip and right_ankle and right_foot_tip:
                    self.x_min = int(min(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1])
                    self.x_max = int(max(left_ankle.x, right_ankle.x, left_foot_tip.x, right_foot_tip.x) * frame.shape[1])
                    self.y_min = int(min(left_hip.y, right_hip.y) * frame.shape[0])
                    self.y_max = int(max(left_ankle.y, right_ankle.y, left_foot_tip.y, right_foot_tip.y) * frame.shape[0])

                    self.x_min -= 50
                    self.y_min -= 70
                    self.x_max += 50
                    self.y_max += 60

                    self.mp_drawing.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                    cv2.rectangle(frame, (self.x_min, self.y_min), (self.x_max, self.y_max), (0, 255, 0), 2)

                    bounding_box_content = frame[self.y_min:self.y_max, self.x_min:self.x_max]
                    imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255

                    if bounding_box_content.size > 0:
                        content_height, content_width, _ = bounding_box_content.shape
                        aspect_ratio = content_height / content_width

                        if aspect_ratio > 1:
                            k = self.imgSize / content_height
                            wCal = math.ceil(k * content_width)
                            imgResize = cv2.resize(bounding_box_content, (wCal, self.imgSize))
                            wGap = math.ceil((500 - wCal) / 2)
                            imgWhite[:, wGap:wCal + wGap] = imgResize
                        else:
                            k = self.imgSize / content_width
                            hCal = math.ceil(k * content_height)
                            imgResize = cv2.resize(bounding_box_content, (self.imgSize, hCal))
                            hGap = math.ceil((500 - hCal) / 2)
                            imgWhite[hGap:hCal + hGap, :] = imgResize

                        imgWhite = cv2.cvtColor(imgWhite, cv2.COLOR_BGR2RGB)

                    self.imgWhite = imgWhite  # Store imgWhite in the class for later use

                cv2.putText(frame, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

            if not self.paused:
                self.root.after(30, self.update)

            current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.scale.set(current_frame)

    def play_pause(self):
        self.paused = not self.paused
        if not self.paused:
            self.update()

    def set_position(self, event):
        value = self.scale.get()
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, value)
        self.update()

    def save_image(self):
        directory = "Data_collection/data/Phase1"
        if not os.path.exists(directory):
            os.makedirs(directory)

        base_name = "Phase1.jpg"
        file_name, file_extension = os.path.splitext(base_name)
        file_path = os.path.join(directory, base_name)
        count = 1

        while os.path.exists(file_path):
            file_path = os.path.join(directory, f"{file_name}_{count}{file_extension}")
            count += 1

        cv2.imwrite(file_path, self.imgWhite)
        print(f"Image saved to {file_path}")

def main():
    root = tk.Tk()
    video_path = 'Data_collection/videos/vid1.mp4' # Replace with your video file path
    app = VideoPlayer(root, video_path)
    root.mainloop()

if __name__ == "__main__":
    main()
