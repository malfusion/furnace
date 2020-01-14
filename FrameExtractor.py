import cv2

class FrameExtractor():
    cap = None
    
    
    def __init__(self, filepath, secondsInterval = 1):
        self.filepath = filepath
        self.secondsInterval = secondsInterval
        self.prevSec = -1 * secondsInterval
        self._openFile()


    def _openFile(self):
        self.cap = cv2.VideoCapture(self.filepath)
        while not self.cap.isOpened():
            cv2.waitKey(1000)

    def getNextFrame(self):
        while True:
            flag, frame = self.cap.read()
            if flag:
                currSec = int(self.cap.get(cv2.CAP_PROP_POS_MSEC) // 1000)
                if currSec >= (self.prevSec + self.secondsInterval):
                    self.prevSec = currSec
                    yield (currSec, frame)
                cv2.waitKey(1)
            else:
                break

    

