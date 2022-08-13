#!/usr/bin/python3
import constants
from webcamDetection import personDetector
from sound import SoundPlayer, Alerts


class turret():
    def __init__(self):
        # detector for finding people through the webcam
        self.detector = personDetector(constants.NETWORK_WEIGHTS_PATH, constants.COCO_CLASS_NAMES, constants.NETWORK_CONFIG_PATH)
        # for playing sounds
        self.soundPlayer = SoundPlayer(constants.SOUNDS_DIR)
        # repreive to give the target a chance to leave
        self.repreive = 3
        # the number of consecutive frames required to lock on to a target
        self.targetFramesLock = 10
        # the threshold for losing a target
        self.targetLosethreshold = 0.5 # if less than 50% of frames detect a person, lose the target
        # start up the turret
        self.start()
    
    def start(self):
        '''Start up the turret'''
        # start up camera
        self.detector.startCamera()
        # play a start up sound
        self.soundPlayer.playAlert(Alerts.ACTIVATE)
        # start main loop
        self.loop()
    
    def stop(self):
        '''shut down the turret'''
        # stop the detector
        self.detector.stop()
        # play shutdown sound
        self.soundPlayer.playAlert(Alerts.DEACTIVATE)

    def targetSpotted(self):
        '''called when a target is spotted'''
        # play a sound
        self.soundPlayer.playAlert(Alerts.TARGET_SPOTTED)

    def targetLost(self):
        '''called when the target is lost'''
        # play a sound
        self.soundPlayer.playAlert(Alerts.TARGET_LOST)

    def loop(self):
        '''the main loop of the turret'''

        # average of detection result over 10 frames, represents the confidence that a person has been detected
        # ranges [0,1]
        detectionAcumulator = 0

        # keep track of if there is a current target
        curTarget = False

        while self.detector.isRunning:
            # get detections
            didDetect, xPos, yPos = self.detector.getDetectionPosSmooth()
            # use the moving average fomula to track the average detection over targetFramesLock frames
            detectionAcumulator = (detectionAcumulator * (1-(1/self.targetFramesLock))) + (int( didDetect) * (1/self.targetFramesLock) )

            # if 100% of the past targetFramesLock frames had a detection
            if ( detectionAcumulator > 0.99 ) & ( curTarget == False ):
                # we've got a target
                self.targetSpotted()
                curTarget = True
                pass

            # if less than targetLosethreshold of the past targetFramesLock frames had a detection
            if ( detectionAcumulator < self.targetLosethreshold ) & curTarget:
                # lost the target
                self.targetLost()
                curTarget = False
                pass

            # if no detections
            if not didDetect:
                # try again
                continue
            
            #print(xPos, yPos)
            # TODO mkae physical system to actually impliment this LOLOLOL
            # make motors turn so that coords are in the center of the webcam

            # if the repreive timer is up and the target is still here,

            # if the coords are close enough to the center, fire

_turret = turret()