import cv2

cam = cv2.VideoCapture(0)

if(cam.isOpened() == False):
	print("Error reading video file")
	
frame_width = int(cam.get(3))
frame_height = int(cam.get(4))

size = (frame_width,frame_height)
name = input("Enter filename:")
result = cv2.VideoWriter(name+'.avi',cv2.VideoWriter_fourcc(*'MJPG'),10,size)

fps = cam.get(cv2.CAP_PROP_FPS)
print("fps:",fps)
input("to start recording press any key")

while True:
	rret, image = cam.read()
	result.write(image)
	cv2.imshow("camera1",image)
	k = cv2.waitKey(1)
	if k != -1:
		break
	
cam.release()
result.release()
cv2.destroyAllWindows()

print("The video was successfully saved")
