# Turret

## Current status

As of current, the framerate of this script on a raspberry pi 3 is ~1FPS, i will solve this by either: 
* Switching to a raspberry pi 4 and seeing if it runs fast enough, or 
* Offloading the object detection to a more powerful computer

The mechanical side of things is still in the design phase \
once a physical design is chosen, motors are chosen, and an electrical layout is chosen, code for controlling motors and such will be developed

## How to install

This repo is made to be installed on a raspberry pi running raspberry pi OS or some other ubuntu based operating system 

clone the repository \
```git clone https://github.com/Scott-McKool/turret.git``` \
enter the repository \
```cd turret``` \
make the install script executable \
``` chmod +x install.sh``` \
run the install script \
```./install.sh```