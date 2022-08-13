# this script is in charge of playing sounds, it

from random import choice
from subprocess import Popen, DEVNULL
from os import listdir, path

class Alerts():
    # the diferent types of alerts to play -> the different directories in the sounds dir
    TARGET_SPOTTED  = "target_spotted.d"
    TARGET_LOST     = "target_lost.d"
    DEACTIVATE      = "deactivate.d"
    ACTIVATE        = "activate.d"

class SoundPlayer():
    def __init__(self, soundDir):
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
        SoundPlayer.playSoundFile(f"{self.soundDir}/{soundFileName}")

    def playAlert(self, alertPath : str):
        # choose a random sound from the apropriate directory
        soundFile = choice(listdir(f"{self.soundDir}/{alertPath}"))
        # get absolute path
        soundFile = f"{self.soundDir}/{alertPath}/{soundFile}"
        # play the sound
        SoundPlayer.playSoundFile(soundFile)
