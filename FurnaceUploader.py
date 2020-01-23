from confluent_kafka import Producer
from FrameExtractor import FrameExtractor
from DataBatcher import DataBatcher
from KafkaUtils import kafkaDeliveryReport
from CVUtils import resizeFrame, showFrame
import datetime
import json
import cv2
import numpy as np
import base64


class FurnaceUploader():
    def __init__(self, configFilePath="./config.json"):
        self.config = self.readConfig(configFilePath)
        self.initProducer()
        

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

    def producerSend(self, data):
        self.kafkaProducer.poll(1.0)
        # b = np.fromstring((json.loads(a))["frame"], 'uint8')
        # p.produce('frames', json.dumps(frameRecord).encode('utf-8'), callback=delivery_report)
        encodedData = json.dumps(data)
        print("Message size", len(encodedData))
        self.kafkaProducer.produce('frames', encodedData, callback=kafkaDeliveryReport)

    def uploadFile(self, filepath, startTime):
        frameExtractor = FrameExtractor(filepath, 1)
        batcher = DataBatcher(keyFunc=batchKeyFun, valFunc=batchValueFun)
        for (sec, frame) in frameExtractor.getNextFrame():
            resizedFrame = resizeFrame(frame, 640, 480) 
            # showFrame(resizedFrame)
            dt = datetime.timedelta(seconds=sec)
            frameTime = startTime + dt

            # START SHORTCIRCUIT BATCHING
            print(resizedFrame.shape)
            frameRecord = {
                "camera": 'camera1',
                "timestamp": str(frameTime),
                "timetype": "second",
                "frame": base64.b64encode(resizedFrame.tobytes()).decode("utf-8")    # While decoding, do numpy.array(json.loads()) 
            }
            self.producerSend(frameRecord)

            # END SHORTCIRCUIT BATCHING
            batcher.addData((frameTime, resizedFrame))
            for batch in batcher.getBatches():
                # Process batch here
                for key, val in batch.items():
                    print("Process batch with key:", key, "and number of frames:", len(val))
        batcher.endBatch()
        for batch in batcher.getBatches():
            # Process last batch here
            for key, val in batch.items():
                print("Process batch with key:", key, "and number of frames:", len(val))
        self.kafkaProducer.flush()
        

def batchKeyFun(data):
    frameTime = data[0]
    return str((frameTime) - datetime.timedelta(seconds=(frameTime).second))

def batchValueFun(data):
    return data[1]

FurnaceUploader("./config.json").uploadFile('./camera_trim.mp4', datetime.datetime(2020,1,14,3,15,30, tzinfo=datetime.timezone.utc))

        


