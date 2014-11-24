#!/bin/bash

echo Black Box Pi setup script
echo

cd /home/pi
sudo apt-get install -y htop bwm-ng gpsd gpsd-clients python-gps sqlite3 python-serial speedometer
sudo gpsctl -f -n /dev/ttyUSB0
sudo rm -rf /home/pi/OBD2SDK_Python
git clone https://github.com/BizDevGeek/OBD2SDK_Python.git
sudo chown -R pi:pi /home/pi/OBD2SDK_Python
sudo cp /home/pi/OBD2SDK_Python/gpslogger.conf /etc/init
sudo cp /home/pi/OBD2SDK_Python/gpssync.conf /etc/init
sudo apt-get install upstart
cd /home/pi/OBD2SDK_Python
python setup.py

