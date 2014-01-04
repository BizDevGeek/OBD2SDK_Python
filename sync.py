import urllib2
import json
import pymongo
from pymongo import MongoClient

#Sync utility. Pull records from buffer (MongoDB) and push to API

#Server globals
WSURLConnectTest = "http://23.239.10.88"
WSURL = WSURLConnectTest + "/obdapi/"

#Buffer
mongodb = "obd"
mongocollection = "pids"

#Check that there's a connection to the API server
def IsConnected(URL):
        try:
		urllib2.urlopen(URL)
	except urllib2.HTTPError, e:
                #print e.code
		return False
	except urllib2.URLError, e:
                #print e.args
		return False
	return True


while True:

	while IsConnected(WSURLConnectTest):

		client = MongoClient()
		db = client[mongodb]
		coll = db[mongocollection]

		i = coll.count()
	
	
		while i <> 0:

			if IsConnected(WSURLConnectTest):
				#get oldest record
				#data = coll.find().sort({_id:1})
				data = coll.find_one()
				id = data['_id']
				#Convert from dict data type retunred by coll.find() into a JSON list data type 
				#Also, remove the _ID item from the array as that's not needed when sending data to the API. 
				jarray = {"APIKey":data['APIKey'], "PID":data['PID'], "PIDValue":data['PIDValue'], "EventDate":data['EventDate']}
				jdata = json.dumps(jarray)
				urllib2.urlopen(WSURL+"save.php", jdata)
				#confirm the record was received by checking the API's return code. If so, delete the record from Mongo
				coll.remove({"_id":id})
				i = coll.count()

	#jdata = {"APIKey":APIKey, "PID":PID, "PIDValue":PIDValue, "EventDate":"2014-01-01 12:00:00"}
	#client = MongoClient()
	#db = client[mongodb]
	#collection = db[mongocollection]
	#post_id = collection.insert(jdata)



