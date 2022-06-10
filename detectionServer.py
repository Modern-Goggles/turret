#!/usr/bin/python3
# this is ment to be run on a computer other than the turret 
# the detection server receives images from the turret, runs object detection on them,
# then send the detection results back to the turret

# right now this is just a test, more work will have to be done to make this easy to use
import socket
import struct
import numpy as np
import cv2

class detectionServer():

    # size of buffer for connection.recv
    RECV_BUFFER_SIZE = 10000

    # images larger than this size in bytes will be assumed to be an error and skipped
    MAX_IMG_SIZE = 100000 # 100kB

    def __init__(self, addr, port, weights, config):
        # the detection network
        self.network = None
        # address (mostly used to specify what interface) to listen on
        self.addr = addr
        # port to listen on
        self.port = port
        # ipv4 TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # make it possible to use an adress already used in the past
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # connection socket to connected remote computer
        self.connection = None
        # get network ready
        self.initalizeNetwork(weights, config)
        # listen
        self.startListening(self.addr, self.port)
        # receive frames and send back detections
        self.serveClient()

    def disconnectClient(self):
        self.connection.send(b"bye")
        self.connection.close()

    def stop(self):
        self.disconnectClient()
        self.socket.close()

    def initalizeNetwork(self, weights, config ):
        self.network = cv2.dnn_DetectionModel(weights, config)
        self.network.setInputSize(320,320)
        self.network.setInputScale(1.0/ 127.5)
        self.network.setInputMean((127.5, 127.5, 127.5))
        self.network.setInputSwapRB(True)

    def receiveFrame(self):
        # an image can be much larger then the size limit of a tcp packet,
        # so first receive the image size, then listen until all the data is retreived

        dataReceived = b""
        # the begining of a string of packets will contain the message size as an int
        # get the size of the begining integer format "L" ( 4 bit integer)
        # the segment containing the message size int
        sizeSegment = struct.calcsize("=L")
        # receive the size of the image
        while len(dataReceived) < sizeSegment:
            dataReceived += self.connection.recv(self.RECV_BUFFER_SIZE)
        # the size of the message stored in the size segment of the packet
        messageSize = dataReceived[:sizeSegment]
        # unpack to integer
        messageSize = struct.unpack("=L", messageSize)[0]
        print(messageSize)
        # if we unpack 4 random bits to an integer, it will likely be very large
        # this will cause the image receiving loop to go on forever. so,
        # if an image size is larger than the max size, just skip it and try again
        if messageSize > self.MAX_IMG_SIZE:
            return None
        
        # where the image data ends
        imageSegment = sizeSegment + messageSize

        # receive the image
        while len(dataReceived) < messageSize:
            dataReceived += self.connection.recv(self.RECV_BUFFER_SIZE)
        # image is from the end of the size segment to the image segment
        image_Bytes = dataReceived[sizeSegment:imageSegment]
        # convert bytes to np array and then a cv2 image
        image = cv2.imdecode(np.frombuffer(image_Bytes, dtype=np.uint8 ), 1 )

        return image

    def getDetections(self, image, detectThreshold : float = 0.5):

        # if image is invalid, return 0,0
        if type(image) != np.ndarray:
            return 0, 0
        # get the output from cv2 dnn
        classIds, confs, bbox = self.network.detect(image,confThreshold=detectThreshold)

        # if there were detections
        if len(classIds):
            for classID, box in zip(classIds.flatten(), bbox):
                # only detect people ( coco classID of 1)
                if classID != 1:
                    continue
                # coords for center of detection
                # xpos = x coordinate + width // 2
                xpos = box[0] + box[2]//2
                # ypos = y coordinate + height // 2
                ypos = box[1] + box[3]//2
                return xpos, ypos

        return 0, 0


    def serveClient(self):
        ''' loop of receiving images, detecting, then sending back results'''
        
        while True:
            try:
                # get frame from clien
                image = self.receiveFrame()
                # detect
                detections = self.getDetections(image)
                # send detections to client
                xpos, ypos = detections
                # show frame
                cv2.rectangle(image, (xpos-15, ypos), (xpos+15, ypos), (50,50,255), 2)
                cv2.rectangle(image, (xpos, ypos-15), (xpos, ypos+15), (50,50,255), 2)
                try:
                    cv2.imshow("image",image)
                except cv2.error:
                    pass
                if cv2.waitKey(1) == ord("q"):
                    self.stop()
                    break

                # construct a message to send the coords as bytes to the client
                xpos = struct.pack("=L", xpos)
                ypos = struct.pack("=L", ypos)
                message = xpos + ypos
                self.connection.sendall(message)
            except ConnectionResetError:
                print("The client reset the connection")
                self.stop()
                break

    def startListening(self, ipAddr, port):
        '''Listen for a connection on a given ip and port'''
        # bind to the address
        self.socket.bind((ipAddr, port ) )
        # listen for incoming connections
        self.socket.listen(1)
        print(f"objectDetector now listening on {ipAddr}:{port}")
        # accept incoming connection
        conn, remoteAddr = self.socket.accept()
        # connection made with ipv4:port
        print(f"connection made with {remoteAddr[0]}:{remoteAddr[1]}")
        self.connection = conn

joe = detectionServer("localhost", 12345, "ssdMobilenetV3/frozen_inference_graph.pb", "ssdMobilenetV3/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")