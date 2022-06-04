#!/usr/bin/python3
import constants
from webcamDetection import personDetector
#import sound

detector = personDetector(constants.NETWORK_WEIGHTS_PATH, constants.COCO_CLASS_NAMES, constants.NETWORK_CONFIG_PATH)

detector.startCamera()
while True:
    x, y = detector.getDetectionPosSmooth()
    print(x, y)
