import cv2
import time
import sys
import numpy as np
from pathlib import Path
import matplotlib




class VideoFramesProcessor:
  
  def __init__(self, filepath):
    super(VideoFramesProcessor,self).__init__()
    self.filepath = filepath
    self.abs_filepath = ''
    self.filepathObj = None
    self.outputDir = './output'
    self.video = None
    self.video_fps = 0
    self.video_frames = 0
    # TODO: change this to time.time() or get on call()
    self.startTimeEpoch = 1518513474 #int(time.time())
    self.frameProcessorData = {}
    
    self.checkFileExists()
    self.checkFileMetaData()

  def setOutputDir(self, outputDir):
    self.outputDir = outputDir

  def setStartTimeEpoch(self, startTimeEpoch):
    self.startTimeEpoch = startTimeEpoch

  def checkFileExists(self):
    if(self.filepath==None or self.filepath==""):
      print("Filepath was empty or not specified.")
      exit(0)
    else:
      self.filepathObj = Path(self.filepath)
      exists = self.filepathObj.is_file()

      if(exists):
        print("File Exists. Processing \n")
        self.abs_filepath = str(self.filepathObj.absolute())
        return True
      else:
        print("File does not exist. Exiting.")
        sys.exit(0)

  def checkFileMetaData(self):
    self.video = cv2.VideoCapture(self.abs_filepath)
    self.video_fps = self.video.get(cv2.CAP_PROP_FPS)
    self.video_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
    print("Video Path: ", self.abs_filepath)
    print("Video FPS: ", self.video_fps)
    print("Video Frames: ", self.video_frames)
    


  def processFile(self):
    # fps = video.get(cv2.CAP_PROP_FPS)
    # print(fps ,time.time())
    # video.release()
    # 
    
    # Reset current frame cursor
    self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
    framesBuffer = []
    lastEpoch = -1
      
    while True:
      # Flag can be false if unable to read or need more time to buffer or end of file. 
      # So dont use it to break loop.
      flag, frame = self.video.read()
      if flag:
        currentFramePos = self.video.get(cv2.CAP_PROP_POS_FRAMES)
        frameVideoSec = int(self.video.get(cv2.CAP_PROP_POS_MSEC)/1000)
        startEpochSec = self.startTimeEpoch
        frameEpochSec = startEpochSec + frameVideoSec
        # print("Processing frame position:", currentFramePos, " at epoch:", frameEpochSec)
        
        if (frameEpochSec != lastEpoch) and len(framesBuffer)>0:
          self.processFramesWithinMillisecond(framesBuffer, lastEpoch)
          framesBuffer = []
        
        framesBuffer.append(frame)
        lastEpoch = frameEpochSec
        
        # If reached end of file
        if( int(currentFramePos)+1 == self.video_frames):
          # Flush last buffer
          self.processFramesWithinMillisecond(framesBuffer, frameEpochSec)
          framesBuffer = []
          break

  
  def processFramesWithinMillisecond(self, frames, frameEpochSec):
    cv2.waitKey(1)
    if self.frameProcessorData is None or self.frameProcessorData == {}:
      self.frameProcessorData = {
        'fgbg': cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=100, detectShadows=True),
        'kernel': cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)),
        'firstFrame': True,
        'detectionVigor': 40 # 20-80
      }
    
    # We need only to single channel height and width
    msecAggregate = np.zeros(frames[0].shape[:2])
    for frame in frames:
      print("Parsing frame")
      
      gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      # gray = cv2.GaussianBlur(frame, (11, 11), 2, 2)
      # print(self.frameProcessorData)
      if self.frameProcessorData['firstFrame']:
        #  First frame, detect nothing, so get difference between same frame upon itself
        fgmask = self.frameProcessorData['fgbg'].apply(frame, None, 0.01)  
        fgmask = self.frameProcessorData['fgbg'].apply(frame, None, 0.01) 
        self.frameProcessorData['firstFrame'] = False
        res = np.zeros(gray1.shape)
      else:
        fgmask = self.frameProcessorData['fgbg'].apply(frame, None, 0.01)  
        
      fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, self.frameProcessorData['kernel'])
      # res   += ( self.frameProcessorData['detectionVigor'] * fgmask.astype(np.float64) + gray1.astype(np.float64))
      msecAggregate = msecAggregate + fgmask
      
    # Don't know which to use, average or minmaxRangebind
    # msecAggregate2 = msecAggregate / len(frames)
    msecAggregate = (msecAggregate / msecAggregate.max()) * 255
    msecAggregate = np.array(msecAggregate, dtype = np.uint8)
    cv2.imshow( "video", msecAggregate);
    cv2.imwrite( self.outputDir + "/image" + str(frameEpochSec) + ".jpg", msecAggregate);

    print("Processing ", len(frames), "frames at epoch:", frameEpochSec)

    











if __name__ == '__main__' :
  aggregate = None
  count = 0.0
  for _ in range(10):
    for epochSec in range(1518513483, 1518513530):
      count+=1.0
      filename = "./output/image"+str(epochSec)+".jpg"
      img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
      if aggregate is None:
        aggregate = np.zeros(img.shape)
      aggregate += img

      print(aggregate.max())
      averaged = aggregate/count
      maxed = averaged/averaged.max()


      # cv2.imshow("image", averaged.astype(np.uint8))

      cv2.imshow("image", maxed)

      
      cv2.waitKey(25)

    # # Start default camera
    # video = cv2.VideoCapture("./camera_trim.mp4");
    # fps = video.get(cv2.CAP_PROP_FPS)
    # print(fps ,time.time())
    # video.release()
    # video.get(cv2.CAP_PROP_POS_MSEC)






