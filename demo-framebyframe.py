import numpy as np
import cv2



cap = cv2.VideoCapture("./camera_trim.mp4")
while not cap.isOpened():
    cap = cv2.VideoCapture("./camera_trim.mp4")
    cv2.waitKey(1000)
    print("Wait for the header")

pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)


while True:
    try:
        _, f = cap.read()
        f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        f = cv2.GaussianBlur(f, (11, 11), 2, 2)
        cnt = 0
        res = 0.05*f
        res = res.astype(np.float64)
        break
    except:
        print('s')


fgbg = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=100,
                                          detectShadows=True)




kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (13, 13))
cnt = 0
sec = 0

while True:
    flag, frame = cap.read()
    if flag:
        # The frame is ready and already captured
        fgmask = fgbg.apply(frame, None, 0.01)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # if cnt == 30: res
        gray = cv2.GaussianBlur(gray, (11, 11), 2, 2)
        gray = gray.astype(np.float64)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        fgmask = fgmask.astype(np.float64)
        # This is dependent on previous iteration
        res += (40 * fgmask + gray)
        cv2.imshow('origvideo', fgmask)
        res_show = res / res.max()
        res_show = np.floor(res_show * 255) 
        res_show = res_show.astype(np.uint8)
        res_show1 = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)
        cv2.imshow('video', res_show1)
        
        
        # res_show2 = cv2.applyColorMap(res_show, cv2.COLORMAP_OCEAN)
        
        
        # cv2.imshow('video2', res_show2)
        
        pos_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)
        print(str(pos_frame)+" frames")
        # if(pos_frame%4==0):
        #   res_show = res / res.max()
        #   res_show = np.floor(res_show * 255) 
        #   res_show = res_show.astype(np.uint8)
        #   res_show1 = cv2.applyColorMap(res_show, cv2.COLORMAP_JET)
        #   cv2.imshow('video', res_show1)
        # if(pos_frame%10==0):
        #   res_show3 = cv2.applyColorMap(res_show, cv2.COLORMAP_HOT)  
        #   cv2.imshow('video3', res_show3)
        # if(pos_frame == 600):
        #   cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos_frame-1)
        print("frame is not ready")
        # It is better to wait for a while for the next frame to be ready
        # cv2.waitKey(1000)

    if cv2.waitKey(10) == 27:
        break
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT) - 10:
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break