import cv2

def resizeFrame(frame, width, height):
    return cv2.resize(frame, (width, height)) 

def showFrame(frame):
    return cv2.imshow('video', frame) 
