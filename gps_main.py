import time
import serial
import os
import jnsdk
import logging
import sys
from ConfigParser import *

logging.basicConfig(filename="events.log", format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

c = ConfigParser()

try:
        c.read("config.txt")
        gps_device = c.get("Settings", "gps_device") 
	gps_logging_interval = c.get("Settings", "gps_logging_interval")
except:
        print "Can't open config file. Run setup.py and make sure config.txt is valid"
        sys.exit()      

APIKey = jnsdk.APIKey()
debug = False #or change to True to output GPS data as it comes in. Only use it if this script isn't run in the background. 

while True:
        time.sleep(float(gps_logging_interval))
	#logging.debug("run main gps reader function")

        serialport = serial.Serial(gps_device, 4800, timeout=0.5)
        r = serialport.readlines(1)
        #alternative: r=serialport.readline(), and then loop through entire List that it returns
	if len(r) == 0:
		continue
        line = r[0] #r is a list, print 0th item in the list
        #print "Raw Output: " + line 
        #print line.find("GPGG")

        if line[1:6] == "GPGGA":
                data = line.split(",")
		#logging.debug("Read from GPS receiver: " + str(line))
		if debug == True:
			print line
                	print "UTC: " + data[1]
                	print "Lat: " + data[2]
                	print "N or S: " + data[3]
                	print "Lon: " + data[4]
                	print "E or W: " + data[5]

		try:
			status=jnsdk.SaveGPS(data[2], data[3], data[4], data[5], data[1])
		except:
			logging.error("Failed to run jnsdk.SaveGPS() \n" + str(sys.exc_info()[0]))
			status="critical failure"

		#logging.debug("Attempted to save GPS by gps_main.py. Status=" + status)
		if debug == True:
			print status
		if status != "true":
			logging.warning("Failed to save GPS record: " + str(line))
			#print "failed to save: " + str(line)
