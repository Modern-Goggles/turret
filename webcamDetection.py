#!/bin/python3
#takes a picture with the camera, compressed it, sends it to a server for processing, and gets back the detection location
import cv2
import socket
import struct

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
    
class networkedDetector():
    def __init__(self, addr, port, cameraID):
        # the adress of the server doing the detection
        self.addr = addr
        # the port to connect to
        self.port = port
        # ipv4 TCP socket 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # camera to use for detection
        self.capture = None
        self.startCamera(cameraID)
        # smoothers to smooth out detection position
        self.xSmoother = None
        self.ySmoother = None
        # connect to the server
        self.connectToServer()
        self.isRunning = True

    def connectToServer(self):
        # TODO handle connection errors here
        print(f"Connecting to {self.addr}:{self.port} . . .")
        self.socket.connect((self.addr, self.port))
        print("connected")

    def stop(self):
        print("stopping videoSender")
        self.isRunning = False
        # release captured camera
        if self.capture:
            self.capture.release()

        # close connection
        self.socket.close()

    def startCamera(self, cameraID : int = 0, resolution : tuple = (640, 480)):
        # if a camera is already reserved
        if self.capture:
            # release it 
            self.capture.release()

        # start up the video capture object 
        self.capture = cv2.VideoCapture(cameraID)
        # set buffer to 1 to try and reduce video lag
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # set the desired resolution
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,resolution[0])
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,resolution[1])

    def captureFrame(self):
        # make sure a camera capture is available
        if not self.capture:
            print("No videoCapture source")
            # return false for the sucess var, and None for the frame var
            return False, None

        return self.capture.read()

    def sendImage(self, image):
        # compress and encode into a jpeg numpy array
        _, imgBuffer= cv2.imencode(".jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 25])
        # convert to bytes
        imageBytes = imgBuffer.tobytes()
        # get size of image as 4 byte integer then pack to 4 bytes
        massageSize = struct.pack("=L", len(imageBytes))
        print(len(imageBytes))
        # message is the image's size followed by the image
        dataToSend = massageSize + imageBytes
        # send all the peices till the whole message is sent
        self.socket.sendall(dataToSend)

    def receiveDetections(self):
        # the detection packet is two 4 byte integers, so 8 bytes total
        messageBack = self.socket.recv(8)
        # unpack the two integers
        if messageBack == b"bye":
            print("conecction ended by the server")
            self.stop()
            return None, None
        xpos = struct.unpack("=L",messageBack[:4])[0]
        ypos = struct.unpack("=L",messageBack[4:])[0]
        # convert to int
        xpos = int(xpos )
        ypos = int(ypos )
        # if we got two zero-integers, convert to none
        if xpos == ypos and xpos == 0:
            xpos, ypos = None, None
        
        return xpos, ypos

    def getDetectionPos(self, alpha : float = 1):
        # capture image
        _, image = self.captureFrame()
        # send to server
        self.sendImage(image)
        # get detection
        xpos, ypos = self.receiveDetections()
        # if there were no detections
        if xpos == None:
            return None, None
        # if alpha is 1, just return the raw position
        if alpha == 1:
            return xpos, ypos
        # if alpha is not 1, use smoothing
        # if smoothers are missing, initialize them 
        if self.xSmoother == None:
            self.xSmoother = smoother(alpha )

        if self.ySmoother == None:
            self.ySmoother = smoother(alpha )
        
        # smooth out the coords of the detection
        xpos = round(self.xSmoother.smooth(xpos ) )
        ypos = round(self.ySmoother.smooth(ypos ) )
        return xpos, ypos