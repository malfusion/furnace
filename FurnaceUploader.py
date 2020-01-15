from confluent_kafka import Producer
from FrameExtractor import FrameExtractor
import cv2
import json

class FurnaceUploader():
    def __init__(self, configFilePath="./config.json"):
        self.config = self.readConfig(configFilePath)
        self.kafkaProducer = self.initProducer()
        

    def readConfig(self, filepath):
        config = {}
        with open(filepath) as json_config:
            config = json.load(json_config)
        return config


    def initProducer(self):
        if "kafka_producer" in self.config:
            self.kafkaProducer = Producer(self.config["kafka_producer"])
        else:
            raise Exception("Cannot find Kafka Producer configuration.")

    def uploadFile(self, filepath):
        frameExtractor = FrameExtractor(filepath, 1)
        for (sec, frame) in frameExtractor.getNextFrame():
            resizedFrame = _resizeFrame(frame, 640, 480) 
            _showFrame(resizedFrame)




def _kafkaDeliveryReport(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

def _resizeFrame(frame, width, height):
    return cv2.resize(frame, (width, height)) 

def _showFrame(frame):
    return cv2.imshow('video', frame) 



FurnaceUploader("./config.json").uploadFile('./camera_trim.mp4')
        


