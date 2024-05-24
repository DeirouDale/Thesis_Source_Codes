import cv2
import mediapipe as mp

def count_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    return total_frames

if __name__ == "__main__":
    video_path = 'Data_process/Right_vid.avi'
    total_frames = count_frames(video_path)
    print(f"Total frames in {video_path}: {total_frames}")
