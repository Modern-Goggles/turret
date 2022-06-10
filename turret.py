#!/usr/bin/python3
import constants
from webcamDetection import networkedDetector
#import sound

detector = networkedDetector(constants.DETECTION_SERVER_IP, constants.DETECTION_SERVER_PORT, 0)

detector.startCamera()
while detector.isRunning:
    x, y = detector.getDetectionPos(0.3)
    print(x, y)
