import urllib2
import json
#import pymongo
#from pymongo import MongoClient
from time import strftime
from ConfigParser import *
import sys
import sqlite3
import datetime

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
#mongodb = c.get("Settings", "mongodb")
#MCOBD = c.get("Settings", "mongocoll_obd")
#MCGPS = c.get("Settings", "mongocoll_gps")
sqlite_gps_db = c.get("Settings", "sqlite_gps_db")
sqlite_obd_db = c.get("Settings", "sqlite_obd_db")

#NOTE: There is no validation of the API key at the client side. Add this in. 
def SendPID(PID, PIDValue):	
	#global APIKey

	#Stop calling the API directly, and instead, push the data into a local buffer via MongoDB.
	#jdata = {"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":"2014-01-01 12:00:00"}
	#jdata = {"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":strftime("%Y-%m-%d %H:%M:%S")}
	#client = MongoClient()
	#db = client[mongodb]
	#collection = db[MCOBD]
	#post_id = collection.insert(jdata)


        #SQLite code:
        try:
                conn = sqlite3.connect(sqlite_obd_db)
        except:
                return "Failed to connect to db"

        curs = conn.cursor()
        curs.execute("insert into readings (pid, pidvalue, eventdate) values((?), (?), (?));", (PID, PIDValue, strftime("%Y-%m-%d %H:%M:%S")))

        try:
                conn.commit()
        except:
                return "Failed to insert record"

        conn.close()

        return "true"


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
	#Saves GPS data to local storage buffer.

        #jdata = {"APIKey":APIKey, "lat":latitude, "NS":NS, "lon":longitude, "EW":EW, "EventDate":strftime("%Y-%m-%d %H:%M:%S")}
        #MongoDB code:
	#client = MongoClient()
        #db = client[mongodb]
        #collection = db[MCGPS]
        #post_id = collection.insert(jdata)
	
	#Validate input
	#Sometimes the GPS outputs bad data, so it's critical to validate input, otherwise over a period of time there WILL be invalid arguments passed.
	if NS != "N" and NS != "S":
		return "Invalid NS"
	if EW != "E" and EW != "W":
		return "Invalid EW"
	
	try:
		float(latitude)
	except:
		return "Invalid LAT"
	try:
		float(longitude)
	except:
		return "Invalid LON"

	#if not isinstance(latitude, float):
		#return "Invalid LAT"

	#not using the UTC arg at this time 
	#try:
		#datetime.datetime.strptime(UTC, "%Y-%m-%d")
	#except ValueError:
		#return "Invalid UTC"	

	#SQLite code:
	try:
		conn = sqlite3.connect(sqlite_gps_db)
	except:
		return "Failed to connect to db"

	curs = conn.cursor()
	curs.execute("insert into gps (lat, ns, lon, ew, eventdate) values((?), (?), (?), (?), (?));", (latitude, NS, longitude, EW, strftime("%Y-%m-%d %H:%M:%S")))	

	try:
		conn.commit()
	except:
		return "Failed to insert record"

	conn.close()

	return "true"
