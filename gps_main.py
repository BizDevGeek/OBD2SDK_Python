import time
import serial
import os

while True:
        time.sleep(1)

        serialport = serial.Serial("/dev/ttyUSB0", 4800, timeout=0.5)
        r = serialport.readlines(1)
        #alternative: r=serialport.readline(), and then loop through entire List that it returns
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

