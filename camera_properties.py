import cv2
import datetime
import paho.mqtt.client as mqtt
import threading
import keyboard
import numpy as np
import time
# Create a VideoCapture object to capture video from the camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Unable to open the camera")
    exit()

# Define the codec and create a VideoWriter object
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
frame_list = []
press_list = []

def camera():
    global frame_list
    frame_count = 0
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        if ret:
            # Write the frame to the output file
            #out.write(frame)
            utc_timestamp = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc).timestamp()
            frame_list.append((frame_count, utc_timestamp))
            # Display the resulting frame
            cv2.imshow('Camera', frame)

            frame_count += 1
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
           break
    cap.release()
    cv2.destroyAllWindows()

def detect_press():
    while True:
        if keyboard.is_pressed('a'):
            utc_timestamp = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=datetime.timezone.utc).timestamp()
            press_list.append(utc_timestamp)
        if keyboard.is_pressed('q'):
            break
# thread1 = threading.Thread(target=camera)
# thread2 = threading.Thread(target=detect_press)

#thread1.start()
#thread2.start()


#thread1.join()
#thread2.join()


#should be the same length
sample_camera_frame = []
sample_camera_time = []

#should be the same length
sample_state_data = []
sample_state_time = []

synced_data = []

state = ["000","001","010","011","100","101","110","111"] #rotate

for x in range(0,31):
    xtime= x* 100 #simulate 10 fps
    sample_camera_frame.append(x)
    sample_camera_time.append(xtime)
for x in range(0,46):
    xtime = x * 66.66 #simulate 15 fps
    sample_state_data.append(state[x%8]) #rotate each data
    sample_state_time.append(xtime)

# for x in range(0,len(sample_camera_frame)):
#     print(sample_camera_frame[x], sample_camera_time[x])
# for x in range(0,len(sample_state_data)):
#     print(sample_state_data[x], sample_state_time[x])


def find_closest(input, reference_list):
    return min(reference_list, key=lambda d: abs(d - input))


for index, xtime in enumerate(sample_camera_time):
    matched_sensor_time = find_closest(xtime, sample_state_time)
    # print(abs(matched_sensor_time-xtime))
    if abs(matched_sensor_time-xtime) > 333: #when esp delay is greater than 1/3 of a second
        matched_sensor_time = "Unknown"
    
    matched_sensor_index = sample_state_time.index(matched_sensor_time)
    synced_data.append((sample_camera_frame[index], sample_state_data[matched_sensor_index],xtime, matched_sensor_time))

print(*synced_data, sep="\n")
hello =time.time()
print(hello)