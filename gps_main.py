import time
import serial
import os
import jnsdk
from ConfigParser import *

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
        time.sleep(gps_logging_interval)

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
		if debug == True:
			print line
                	print "UTC: " + data[1]
                	print "Lat: " + data[2]
                	print "N or S: " + data[3]
                	print "Lon: " + data[4]
                	print "E or W: " + data[5]
		status=jnsdk.SaveGPS(data[2], data[3], data[4], data[5], data[1])
		#if status != "true":
			#print "failed to save: " + str(line)
