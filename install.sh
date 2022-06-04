#!/usr/bin/bash
# ths script installs the turret repo with the required dependencies and files

# install dependencies
sudo apt update 
sudo apt install python3-opencv=4.5.1+dfsg-5 mpv=0.32.0-3 -y

# set the repo directory variable (REPO_DIR) in constants.py to the current directory
sed -i "s|REPO_DIR = ''|REPO_DIR = '$PWD'|" constants.py

# download network data
wget https://github.com/Scott-McKool/turret/releases/download/downloads/ssdMobilenetV3.zip
# make folder to put contents in
mkdir ssdMobilenetV3
# extract to folder
unzip ssdMobilenetV3.zip -d ssdMobilenetV3/
# clean up and remove the zip archive
rm ssdMobilenetV3.zip

# download sounds
wget https://github.com/Scott-McKool/turret/releases/download/downloads/sounds.zip
# make folder to put contents in
mkdir sounds
# extract to folder
unzip sounds.zip -d sounds/
# clean up and remove the zip archive
rm sounds.zip

# make the main file executable
chmod +x turret.py