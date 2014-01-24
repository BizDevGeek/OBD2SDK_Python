import urllib2
import json
import pymongo
from pymongo import MongoClient
import time
from ConfigParser import *
import jnsdk
import sqlite3

c = ConfigParser()
c.read("config.txt")

WSURL = c.get("Settings", "url")
APIKey = jnsdk.APIKey()

#Buffer
db = c.get("Settings", "sqlite_obd_db")

#Sync utility. Pull records from buffer and push to API

#Server globals
WSURLConnectTest = WSURL

#Other Settings
CheckInterval = 1 #seconds

#Check that there's a connection to the API server
def IsConnected(URL):
        try:
		urllib2.urlopen(URL)
	except urllib2.HTTPError, e:
                #print e.code
		if e.code == 403:
			return True #server's online, just not letting that directory be browsed
		return False
	except urllib2.URLError, e:
                #print e.args
		return False
	return True


while True:
	time.sleep(CheckInterval) #check for an internet connection to server every N seconds
	while IsConnected(WSURLConnectTest):


                conn = sqlite3.connect(db)
                curs = conn.cursor()

                curs.execute("select count(*) from readings")
                row = curs.fetchone()
                i = row[0]

		while i <> 0:

			if IsConnected(WSURLConnectTest):


                                #get oldest record
				#Ideally start from oldest record, but this is a major performance hit as written currently. Removed it for now.
				#curs.execute("select PID, PIDValue, eventdate, id from readings order by eventdate")
                                curs.execute("select PID, PIDValue, eventdate, id from readings")
				row = curs.fetchone()
                                id = row[3] 
                                jarray = {"APIKey":APIKey, "PID":row[0], "PIDValue":row[1],"EventDate":row[2]}
                                jdata = json.dumps(jarray)
                                #print "Uploading: " + jdata
                                result = urllib2.urlopen(WSURL+"save.php", jdata)
                                r = result.read()
                                if r == "true":
                                        #confirm the record was received by checking the API's return code. If so, delete the record from db
                                        curs.execute("delete from readings where id = (?)", (id,))
                                        conn.commit()
                                        curs.execute("select count(*) from readings")
                                        row = curs.fetchone()
                                        i = row[0]
                                else:
                                        #API isn't saving the data. Log or alert the system to this.
                                        print "Failed to upload. ID="+str(id)+r 

