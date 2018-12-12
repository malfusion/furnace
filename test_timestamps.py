import cv2
import time
 
if __name__ == '__main__' :
 
    # Start default camera
    video = cv2.VideoCapture("./camera_trim.mp4");
    fps = video.get(cv2.CAP_PROP_FPS)
    print(fps ,time.time())
    video.release()
    video.get(cv2.CAP_PROP_POS_MSEC)
