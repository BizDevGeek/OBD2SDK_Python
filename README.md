OBD2SDK_Python
==============

Python SDK for using the OBD2 cloud storage service

Main project page: http://www.blackboxpi.com

The OBD2 cloud storage service is available here: https://github.com/BizDevGeek/OBD2CloudStorage

This project contains an SDK that you can use to save OBD2 PID values. Use it with existing Python based OBD2 capture software such as the popular "pyobd". Any time a PID is logged from the computer, save it using the SDK so that it gets stored in the cloud storage service.  

The SDK stores the saved values in a local buffer. The buffer is a MongoDB collection. 

GPS data is also being added in. This feature is still in development. 

sync.py pulls records from the local buffer and sends them to the API via JSON. It then removes them from the buffer. Runs in an infinite loop, not just until the buffer is empty. You can run it in a separate terminal window and leave it going, or Ctrl+C to kill it. 

The date/time reported to the cloud service is based on the Pi's local time and timezone. Make sure this is set properly. You can run "sudo raspi-config" to set the timezone on your Pi. In future versions, the UTC clock returned by the GPS may be used, although this can also have issues. 


Installation

SSH into your Raspberry Pi

Make sure it's up to date:

sudo apt-get update

sudo apt-get upgrade

Install the various pre-requisites:

sudo apt-get install gpsd gpsd-clients python-gps python-serial sqlite3

cd /home/pi

Copy the SDK from GitHub to the Pi:

git clone https://github.com/BizDevGeek/OBD2SDK_Python.git

Run the setup program. This gets you an API key from the cloud service, sets the names of the databases, and the device path to an optional GPS device. The config data is saved to config.txt. You can use all the defaults to keep it simple. 

python setup.py

Install the GPS daemon so that it's recording GPS data into the local buffer. The daemon uses "upstart" instead of /etc/init.d, the latest method of managing services in Linux. 

sudo cp /home/pi/OBD2SDK_Python/gpslogger.conf /etc/init

sudo service gpslogger start

If you're installing the API to your own server, make sure that's setup first. You'll need the URL for the next step. EX: http://23.239.10.88/obdapi/. If you don't have this setup, a default server is provided for you. 

setup.py - Prompts you for the server URL (or use the author's for default) and for an email address and returns an API Key for you to use. It creates the config file below.

config.txt - Created by setup.py. Contains the URL of the API server and your API Key for the SDK. 

Using the SDK

Copy the .py files to where your Python program is. 

In your Python program, add "import jnsdk". To save a PID each time you poll it from the OBD2 serial connection: jnsdk.SendPID(jnsdk.APIKey(), PID, PIDValue)

The above function call saves the PID values to a local buffer, a MongoDB Collection. Run sync.py to sync the data to the API. It pulls records one at a time from the buffer, uploads to the API, then removes them. It verifies that there's a connection to the server first. 

The GPS daemon gpslogger reads the Pi's serial connection to the USB GPS device and logs it to local buffer. Run sync_gps.py to sync the data from local storage buffer into the cloud. 

