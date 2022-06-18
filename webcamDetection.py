#!/bin/python3
#runs detection on webcam and smooths coordinates of the resulting detection
import cv2

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
    
# class for detecting people using computer vision on a given webcam
class personDetector():
    def __init__(self, netWeights, netLabels, netConfig, smootherAlpha : float = 0.3):
        # config variables
        self.weights = netWeights
        self.labels = netLabels
        self.config = netConfig
        # camera capture object
        self.capture = None
        # ddn detector object
        self.network = None
        self.initalizeNetwork()
        # smoothers
        self.xSmoother = None
        self.ySmoother = None
        # used to mark when detector is running
        self.isRunning = False

    def initalizeNetwork(self):
        self.network = cv2.dnn_DetectionModel(self.weights, self.config)
        self.network.setInputSize(320,320)
        self.network.setInputScale(1.0/ 127.5)
        self.network.setInputMean((127.5, 127.5, 127.5))
        self.network.setInputSwapRB(True)

    def stop(self):
        # if a camera is already reserved
        if self.capture:
            # release it 
            self.capture.release()
        # set to not running
        self.isRunning = False

    def startCamera(self, cameraID : int = 0, resolution : tuple = (640, 480)):
        # if a camera is already reserved
        if self.capture:
            # release it 
            self.capture.release()

        # start up the video capture object 
        self.capture = cv2.VideoCapture(cameraID)
        # set the desired resolution
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1])
        # set buffer to small value to minimize delay 
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # mark as running 
        self.isRunning = True

    def captureFrame(self):
        # make sure a camera capture is available
        if not self.capture:
            print("No videoCapture source")
            # return false for the sucess var, and None for the frame var
            return False, None

        return self.capture.read()

    def getDetectionPos(self, detectThreshold : float = 0.5):
        # capture image
        _, frame = self.captureFrame()

        # run detection
        classIds, confs, bbox = self.network.detect(frame,confThreshold=detectThreshold)

        # if at least one detection
        if len(classIds) > 0:
            # loop through detections 
            for classId, confidence, box in zip(classIds.flatten(),confs.flatten(),bbox):
                # only detect people (coco class id of 1)
                if classId != 1:
                    continue
                # coords for center of detection
                # xpos = x coordinate + width // 2
                xpos = box[0] + box[2]//2
                # ypos = y coordinate + height // 2
                ypos = box[1] + box[3]//2
                return True, xpos, ypos
        
        return False, None, None

    def getDetectionPosSmooth(self, ALPHA : float = 0.3, detectThreshold : float = 0.5):
        # initalize smoothers
        if not self.xSmoother:
            self.xSmoother = smoother(ALPHA)

        if not self.ySmoother:
            self.ySmoother = smoother(ALPHA)

        # get pos from 1 frame
        didDetect, x, y = self.getDetectionPos(detectThreshold)

        if not didDetect:
            return False, None, None

        # smooth over 1/ALPHA frames
        self.xPos = self.xSmoother.smooth(x)
        self.yPos = self.ySmoother.smooth(y)

        # return smoothed position
        return True, self.xPos, self.yPos
