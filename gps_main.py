import time
import serial
import os
import jnsdk
from ConfigParser import *

c = ConfigParser()

try:
        c.read("config.txt")
        gps_device = c.get("Settings", "gps_device") 
except:
        print "Can't open config file. Run setup.py and make sure config.txt is valid"
        sys.exit()      

APIKey = jnsdk.APIKey()

while True:
        time.sleep(1)

        serialport = serial.Serial(gps_device, 4800, timeout=0.5)
        r = serialport.readlines(1)
        #alternative: r=serialport.readline(), and then loop through entire List that it returns
	if len(r) == 0:
		continue
        line = r[0] #r is a list, print 0th item in the list
        #print "Raw Output: " + line 
        #print line.find("GPGG")

        if line[1:6] == "GPGGA":
                #print "HIT"
                data = line.split(",")
                #print "UTC: " + data[1]
                #print "Lat: " + data[2]
                #print "N or S: " + data[3]
                #print "Lon: " + data[4]
                #print "E or W: " + data[5]
		jnsdk.SaveGPS(APIKey, data[2], data[3], data[4], data[5], data[1])

