#!/bin/bash

echo Black Box Pi setup script
echo 

cd /home/pi
sudo apt-get install -y htop bwm-ng gpsd gpsd-clients python-gps sqlite3 python-serial speedometer
sudo apt-get install -y apache2 php5 libapache2-mod-php5 php5-sqlite
sudo gpsctl -f -n /dev/ttyUSB0
sudo rm -rf /home/pi/OBD2SDK_Python
git clone https://github.com/BizDevGeek/OBD2SDK_Python.git
sudo chown -R pi:pi /home/pi/OBD2SDK_Python
sudo rm /var/www/index.html
sudo cp /home/pi/OBD2SDK_Python/index.php /var/www
sudo cp /home/pi/OBD2SDK_Python/gpslogger.conf /etc/init
sudo cp /home/pi/OBD2SDK_Python/gpssync.conf /etc/init
sudo apt-get install upstart
cd /home/pi/OBD2SDK_Python
python setup.py

