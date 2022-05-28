#!/bin/python3
#runs detection on webcam and writes position to stdout for testing
import cv2
import detectConfig

# detection threshold
THRESHOLD = 0.5

# id of v4l2 device 
CAMERA_ID = 0

# capture camera
capture = cv2.VideoCapture(CAMERA_ID)

# adjust settings
capture.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
capture.set(cv2.CAP_PROP_BRIGHTNESS,70)

 
net = cv2.dnn_DetectionModel(detectConfig.NETWORK_WEIGHTS_PATH,detectConfig.NETWORK_CONFIG_PATH)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# class to smooth out position of detection across frames to avoid shakey aim
# basically just the moving average function
class smoother():
    def __init__(self, alpha : float):
        self.alpha = alpha
        self.accumulator = -1
    
    def smooth(self, value):
        if self.accumulator == -1:
            self.accumulator = value
        self.accumulator = (self.alpha * value) + ((1.0 - self.alpha) * self.accumulator)
        return self.accumulator
    
xpos = 0
ypos = 0

SMOOTHER_ALPHA = 0.3

xSmoother = smoother(SMOOTHER_ALPHA)
ySmoother = smoother(SMOOTHER_ALPHA)

while True:
    # capture an image
    _, img = capture.read()

    # run detection on the image
    classIds, confs, bbox = net.detect(img,confThreshold=THRESHOLD)

    # if at least one detection
    if len(classIds) > 0:
        # loop through detections 
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            # only detect people (coco class id of 1)
            if classId != 1:
                continue
            xpos = round( xSmoother.smooth(box[0] + box[2]//2))
            ypos = round( ySmoother.smooth(box[1] + box[3]//2))
            print(f"Person at {xpos}, {ypos}")

capture.release()
