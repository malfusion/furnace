import numpy as np
import cv2
import matplotlib
import time

cap = cv2.VideoCapture("./camera_trim.mp4")
while not cap.isOpened():
    cap = cv2.VideoCapture("./camera_trim.mp4")
    cv2.waitKey(1000)
    print("Wait for the header")

print(cv2.getBuildInformation())

pos_frame = cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

fgbg = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=100, detectShadows=True)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
first = True

start = time.time()

while True:
    flag, frame = cap.read()
    if flag:
        
        gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(frame, (11, 11), 2, 2)
        if first:
          #  First frame, detect nothing, so get difference between same frame upon itself
          fgmask = fgbg.apply(frame, None, 0.01)  
          fgmask = fgbg.apply(frame, None, 0.01) 
          first = False
          res = np.zeros(gray1.shape)
        else:
          fgmask = fgbg.apply(frame, None, 0.01)  
          
        detectionVigor = 40 # 20-80
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        res   += ( detectionVigor * fgmask.astype(np.float64) + gray1.astype(np.float64))
        

        # cv2.imwrite( "./diffs/image"+str(cap.get(cv2.CAP_PROP_POS_FRAMES))+".jpg", fgmask);
        # colored = 0
        # for i in range(len(fgmask)):
        #   for j in range(len(fgmask[i])):
        #     if(fgmask[i][j]>0):
        #       print(fgmask[i][j])

        # cv2.imshow('origvideo2', fgmask)
        # res_show2 = cv2.applyColorMap(res_show, cv2.COLORMAP_OCEAN)
        pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        print(str(pos_frame)+" frames")
        if(pos_frame%100==0):
          print("updating1")
          res_show = res / res.max()
          res_show = np.floor(res_show * 255) 
          res_show = res_show.astype(np.uint8)
          res_show1 = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)
          cv2.imshow('video', res_show1)
        # if(pos_frame%10==0):
        #   res_show3 = cv2.applyColorMap(res_show, cv2.COLORMAP_HOT)  
        #   cv2.imshow('video3', res_show3)
        # if(pos_frame == 600):
        #   cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        # cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame+3)
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
        print("frame is not ready")
        # It is better to wait for a while for the next frame to be ready
        # cv2.waitKey(1000)

    if pos_frame == 101:
      end = time.time()
      print("Time:", end-start)
    if cv2.waitKey(10) == 27:
        break
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT) - 10:
        res_show = res / res.max()
        res_show = np.floor(res_show * 255) 
        res_show = res_show.astype(np.uint8)
        res_show1 = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)
        cv2.imshow('video', res_show1)
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break