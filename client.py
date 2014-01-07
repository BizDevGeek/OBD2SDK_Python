#Example of how a Python OBD2 program can use the SDK
#This fills up the local buffer with sample PID data. The buffer is a MongoDB Collection. 
#After this script runs for a little while, use sync.py to pull the data out of the buffer and send it to the API. 

import urllib2
import json
import random
import time
import jnsdk

#Simulate polling taking place every X seconds so it sends a flood of data to the service.
while True:
	time.sleep(.1)
	
	#arbitrary random values and ranges
	PID = random.randrange(10,99)
	PIDValue = random.randrange(-50, 5000)
	APIKey = jnsdk.APIKey()

	jnsdk.SendPID(APIKey, PID, PIDValue)

