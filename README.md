# Turret

## Current status

I have implimented a networked person detection system in the networkedDetection branch. \
as of right now the raspberry pi can run object detection in this way at about 30 FPS, which his more than enough.

I do think it's kind of lame to have to have an extra coputer and a wifi network to run the turret, so in the future i will probably explore trying to detect people without the use of a neural net. perhaps i could do it with a color mask or something.

The mechanical side of things is still in the design phase \
once a physical design is chosen, motors are chosen, and an electrical layout is chosen, code for controlling motors and such will be developed

## How to install

### requirements
these is just the verions i use, i don't know how far back one could go before it breaks the code \
these are installed automatically by install.sh \
```python3-opencv=4.5.1+dfsg-5``` \
```mpv=0.32.0-3```

### instructions

This repo is made to be installed on a raspberry pi running raspberry pi OS or some other ubuntu based operating system 

clone the repository \
```git clone https://github.com/Scott-McKool/turret.git``` \
enter the repository \
```cd turret``` \
make the install script executable \
```chmod +x install.sh``` \
run the install script \
```./install.sh```

## How to run turret.py on system startup

to have turret.py run on startup \
make the runOnStartUp.sh script executable \
```chmod +x runOnStartUp.sh``` \
run the runOnStartUp.sh script \
```./runOnStartUp.sh```

if you no longer want turret.py to run on startup, use \
```sudo systemctl disable turret.service```
