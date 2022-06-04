# issue a sudo command at the begining so the user gives their sudo password when they run this script instead of halfway through
sudo echo "Setting up turret.py to run on system startup"

# make a unit file for this systemd service
echo "creating unit file 'turret.service'"
    cat > turret.service <<UNITFILE
[Unit]
Description=Runs turret.py script on startup
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 "$PWD/turret.py"

[Install]
WantedBy=multi-user.target
UNITFILE

# move to systemd/system directory
echo "moving unit file to '/etc/systemd/system/turret.service'"
sudo mv turret.service /etc/systemd/system/turret.service

# reload systemd so it can find this newly created service
echo "reloding systemctl daemon"
sudo systemctl daemon-reload

# enable this service in systemd
echo "enabling turret.service"
sudo systemctl enable turret.service

echo "turret service has been added and enabled"
echo "turret.py will be automatically run on startup from now on"
echo ""
echo "to dissable running on startup type 'sudo systemctl disable turret.service'"
echo ""
exit 0