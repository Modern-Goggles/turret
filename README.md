# Turret

## Current status

As of current, the framerate of this script on a raspberry pi 3 is ~1FPS, i will solve this by either: 
* Impliment a simpler detection alorithm, such as color masking and blobing,
* Switching to a raspberry pi 4 and seeing if it runs fast enough, or 
* Offloading the object detection to a more powerful computer

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
