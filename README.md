# Turret

## Current status

As of current, the framerate of this script on a raspberry pi 3 is ~1FPS, i will solve this by either: 
* Switching to a raspberry pi 4 and seeing if it runs fast enough, or 
* Offloading the object detection to a more powerful computer

The mechanical side of things is still in the design phase \
once a physical design is chosen, motors are chosen, and an electrical layout is chosen, code for controlling motors and such will be developed

## How to install

### requirements
this is just the verion i use, i don't know how far back one could go before it breaks \
```opencv-python==4.5.5.64```

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
```./runOnStartUp.sh```\
note : \
systemctl runs this python script as root \
to run a python script as root, the modules it uses have to be installed as root \
it can be unsafe to install pip packages as root, some packages (even ones with 30,000+ downloads) have been found to have [malware in them](https://arstechnica.com/gadgets/2021/07/malicious-pypi-packages-caught-stealing-developer-data-and-injecting-code/) \
furthermore, if you install conflicting versions of the same package it may break programs that depend on those packages. 

**However,** because this is meant for a dedicated raspberry pi, and the only module required is openCV-python. i feel it is safe to install openCV-python as root if you plan on having this script boot on startup. 
