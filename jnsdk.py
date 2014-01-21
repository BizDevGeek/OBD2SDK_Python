import urllib2
import json
import pymongo
from pymongo import MongoClient
from time import strftime
from ConfigParser import *
import sys
import sqlite3

c = ConfigParser()

try:
	c.read("config.txt")
	test = c.get("Settings", "url") #grab a random setting to test/raise the exception
except:
	print "Can't open config file. Run setup.py and make sure config.txt is valid"
	sys.exit()	

WSURL = c.get("Settings", "url")
API_Key = c.get("Settings", "api_key")

#Buffer
mongodb = c.get("Settings", "mongodb")
MCOBD = c.get("Settings", "mongocoll_obd")
MCGPS = c.get("Settings", "mongocoll_gps")
sqlite_db = c.get("Settings", "sqlite_gps_db")

#NOTE: There is no validation of the API key at the client side. Add this in. 
def SendPID(APIKey, PID, PIDValue):	
	#global APIKey

	#Stop calling the API directly, and instead, push the data into a local buffer via MongoDB.
	#jdata = {"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":"2014-01-01 12:00:00"}
	jdata = {"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":strftime("%Y-%m-%d %H:%M:%S")}
	client = MongoClient()
	db = client[mongodb]
	collection = db[MCOBD]
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

def APIKey():
	return API_Key

def SaveGPS(latitude, NS, longitude, EW, UTC):
	#TODO: Validate the data coming in before it's sent out. 

        #jdata = {"APIKey":APIKey, "lat":latitude, "NS":NS, "lon":longitude, "EW":EW, "EventDate":strftime("%Y-%m-%d %H:%M:%S")}
        #MongoDB code:
	#client = MongoClient()
        #db = client[mongodb]
        #collection = db[MCGPS]
        #post_id = collection.insert(jdata)
	
	#SQLite code:
	conn = sqlite3.connect(sqlite_db)
	curs = conn.cursor()
	curs.execute("insert into gps (lat, ns, lon, ew, eventdate) values((?), (?), (?), (?), (?));", (latitude, NS, longitude, EW, strftime("%Y-%m-%d %H:%M:%S")))	
	conn.commit()
	conn.close()
