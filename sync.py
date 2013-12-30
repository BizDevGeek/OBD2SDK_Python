import urllib2
import json
import pymongo
from pymongo import MongoClient

#Sync utility. Pull records from buffer (MongoDB) and push to API

#Server globals
WSURL = "http://23.239.10.88/obdapi/"

#Buffer
mongodb = "obd"
mongocollection = "pids"

client = MongoClient()
db = client[mongodb]
coll = db[mongocollection]

i = coll.count()


while i <> 0:

	#get oldest record
	jdata = coll.find().sort({"_id":1})
	#How to get the _ID value of that record? Need it to delete the record after uploading it to API
	#The _ID value is the first item in the array. Pull it from there to get it. 
	#Also, need to remove the _ID item from the array as that's not needed when sending data to the API. Or can
	#I just leave it and allow the API to ignore it? 
	urllib2.urlopen(WSURL+"save.php", jdata)
	#confirm the record was received by checking the API's return code. If so, delete the record from Mongo
	coll.remove({"_id":"INSERT THE ID HERE"})
	i = coll.count()

	#jdata = json.dumps({"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":"2014-01-01 12:00:00"})
	#Stop calling the API directly, and instead, push the data into a local buffer via MongoDB.
	#urllib2.urlopen(WSURL+"save.php", jdata)
	jdata = {"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":"2014-01-01 12:00:00"}
	client = MongoClient()
	db = client[mongodb]
	collection = db[mongocollection]
	post_id = collection.insert(jdata)



