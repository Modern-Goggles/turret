#!/usr/bin/python3
import constants
from webcamDetection import personDetector
from sound import soundPlayer


class turret():
    def __init__(self):
        # detector for finding people through the webcam
        self.detector = personDetector(constants.NETWORK_WEIGHTS_PATH, constants.COCO_CLASS_NAMES, constants.NETWORK_CONFIG_PATH)
        # for playing sounds
        self.soundPlayer = soundPlayer(constants.SOUNDS_DIR)
        # repreive to give the target a chance to leave
        self.repreive = 3
    
    def start(self):
        '''Start up the turret'''
        # start up camera
        self.detector.startCamera()
        # play a start up sound
        self.soundPlayer.playSound("days_are_numbered.mp4")
        # start main loop
        self.loop()
    
    def stop(self):
        '''shut down the turret'''
        # stop the detector
        self.detector.stop()
        # play shutdown sound
        self.soundPlayer.playSound("end_of_it.mp4")

    def targetSpotted(self):
        '''called when a target is spotted'''
        # play a sound
        self.soundPlayer.targetSpotted()

    def targetLost(self):
        '''called when a target is spotted'''
        # play a sound
        self.soundPlayer.targetLost()

    def loop(self):
        '''the main loop of the turret'''

        # start with no past detections
        lastDidDetect = False

        while self.detector.isRunning:
            # get detections
            didDetect, xPos, yPos = self.detector.getDetectionPosSmooth()

            # if there is a detection but there was not one last loop
            if didDetect and didDetect != lastDidDetect:
                # spotted a target
                self.targetSpotted()

            # if there is not a detection but there was one last loop
            if not didDetect and didDetect != lastDidDetect:
                # lost the target
                self.targetLost()

            # keep result of this detection so that changes can be detected next loop
            lastDidDetect = didDetect

            # if no detections
            if not didDetect:
                # try again
                continue
            
            # TODO mkae physical system to actually impliment this LOLOLOL
            # make motors turn so that coords are in the center of the webcam

            # if the repreive timer is up and the target is still here,

            # if the coords are close enough to the center, fire

