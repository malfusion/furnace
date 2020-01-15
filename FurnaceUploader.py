from confluent_kafka import Producer
from FrameExtractor import FrameExtractor
from KafkaUtils import kafkaDeliveryReport
from CVUtils import resizeFrame, showFrame
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
            resizedFrame = resizeFrame(frame, 640, 480) 
            showFrame(resizedFrame)






FurnaceUploader("./config.json").uploadFile('./camera_trim.mp4')
        


