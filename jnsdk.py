import urllib2
import json

#User Info
#APIKey = "003"

#Server globals
WSURL = "http://23.239.10.88/obdapi/"

#NOTE: There is no validation of the API key at the client side. Add this in. 
def SendPID(APIKey, PID, PIDValue):	
	#global APIKey

	jdata = json.dumps({"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":"2014-01-01 12:00:00"})
	urllib2.urlopen(WSURL+"save.php", jdata)

def RegisterNewUser(Email):
	#adds new user and gets his API key

	jdata = json.dumps({"Email":Email})
	result = urllib2.urlopen(WSURL+"register.php", jdata)
	data = json.load(result)
	return data

def RetrieveKey(Email):
	#emails the API key to the email given

        jdata = json.dumps({"Email":Email})
        urllib2.urlopen(WSURL+"retrievekey.php", jdata)
