from subprocess import Popen, DEVNULL
from os import path

def playSoundFile(soundFile):
    '''Spawn a new process that plays a sound file with mpv'''
    # get path to given sound file
    soundFile = path.abspath(soundFile)
    # ensure it exists
    if not path.exists(soundFile):
        print(f"Cannot play sound, no such file {soundFile}")
        return
    # because this makes a new process and get piped to dev null, print that this sound is playing for logging purposes
    print(f"playing sound {soundFile}")
    # spawn a new process to use mpv to play the sound file
    # use nohup to prevent the process from ending on hang up
    Popen(["nohup", "mpv", "--no-video", f"{soundFile}"], stdout=DEVNULL, stderr=DEVNULL)
