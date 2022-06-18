from random import choice
from subprocess import Popen, DEVNULL
from os import listdir, path
from time import time
import constants

class soundPlayer():
    def __init__(self, soundDir):
        # time to wait after playing a sound before playing another
        self.soundCooldown = 3

        # the last time a sound was played
        self.lastSound = 0

        # the directory for sounds
        self.soundDir = soundDir

    def playSoundFile(soundFile):
        '''Spawn a new process that plays a sound file with mpv'''
        # get path to given sound file
        soundFile = path.abspath(soundFile)
        # ensure it exists
        if not path.exists(soundFile):
            print(f"Cannot play sound, no such file {soundFile}")
            return False
        # because this makes a new process and get piped to dev null, print that this sound is playing for logging purposes
        print(f"playing sound {soundFile}")
        # spawn a new process to use mpv to play the sound file
        # use nohup to prevent the process from ending on hang up
        Popen(["nohup", "mpv", "--no-video", f"{soundFile}"], stdout=DEVNULL, stderr=DEVNULL)
        return True

    def playSound(self, soundFileName):
        self.playSoundFile(f"{self.soundDir}/{soundFileName}")

    # TODO refactor these methods to reduce the ammount of repeated code
    def targetSpotted(self):
        '''play a sound signifying that a target has been spotted'''
        # if the cooldawn has yet to pass
        if time() - self.lastSound < self.soundCooldown:
            # don't play a sound
            return False
        # if the cooldown has passed
        # choose a sound
        soundFile = choice(listdir(f"{self.soundDir}/target_spotted"))
        # starrt playing it
        if self.playSoundFile(soundFile):
            # if the soundplay returned true
            # mark the time 
            self.lastSound = time()
            # pass through the true return to signify sucess
            return True
        # return false to signify failure
        return False

    def targetLost(self):
        '''play a sound signifying that a target has been spotted'''
        # if the cooldawn has yet to pass
        if time() - self.lastSound < self.soundCooldown:
            # don't play a sound
            return False
        # if the cooldown has passed
        # choose a sound
        soundFile = choice(listdir(f"{self.soundDir}/target_lost"))
        # starrt playing it
        if self.playSoundFile(soundFile):
            # if the soundplay returned true
            # mark the time 
            self.lastSound = time()
            # pass through the true return to signify sucess
            return True
        # return false to signify failure
        return False