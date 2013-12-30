import urllib2
import json
import pymongo
from pymongo import MongoClient


#Server globals
WSURL = "http://23.239.10.88/obdapi/"

#Buffer
mongodb = "obd"
mongocollection = "pids"

#NOTE: There is no validation of the API key at the client side. Add this in. 
def SendPID(APIKey, PID, PIDValue):	
	#global APIKey

	#jdata = json.dumps({"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":"2014-01-01 12:00:00"})
	#Stop calling the API directly, and instead, push the data into a local buffer via MongoDB.
	#urllib2.urlopen(WSURL+"save.php", jdata)
	jdata = {"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":"2014-01-01 12:00:00"}
	client = MongoClient()
	db = client[mongodb]
	collection = db[mongocollection]
	post_id = collection.insert(jdata)



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
