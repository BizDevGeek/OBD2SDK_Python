#Jozef Nagy
#1/2014
#Sets up the SDK to use the API. It establishes the URL of the API server and gets an API Key for the SDK to use. 

import sys
from ConfigParser import *
import jnsdk
import re #regex
import sys

f = open("config.txt", "w")

c = ConfigParser()

print "Setup for the SDK"
print "Enter your own server information or use the default server"
print "If you're using your own API server, the API MUST be setup and running before you run this script. Otherwise you won't be able to register yourself to get an API Key"
print "This script will register your email address and provide you with your API key. The API key is needed to use the SDK."

apiurl = raw_input("Enter the URL of the API to use [Enter for default value: http://23.239.10.88/obdapi/]")

if apiurl == "":
	apiurl = "http://23.239.10.88/obdapi/"

#mongodb = raw_input("Enter the name of the MongoDB to use [Enter for default value: obd]")

#if mongodb == "":
#	mongodb = "obd"

#mongocollection_obd = raw_input("Enter the name of the MongoDB Collection to use for OBD2 [Enter for default value: pids]")

#if mongocollection_obd == "":
#	mongocollection_obd = "pids"

#mongocollection_gps = raw_input("Enter the name of the MongoDB Collection to use for GPS [Enter for default value: gps]")

#if mongocollection_gps == "":
#        mongocollection_gps = "gps"

sqlite_gps_db = raw_input("Enter the name of the SQLite database to use for GPS [Enter for default value: gps.db]")

if sqlite_gps_db == "":
        sqlite_gps_db = "gps.db"

sqlite_obd_db = raw_input("Enter the name of the SQLite database to use for OBD2 [Enter for default value: obd.db]")

if sqlite_obd_db == "":
        sqlite_obd_db = "obd.db"

gps_device = raw_input("Enter the Linux device name of your USB GPS [Enter for default value: /dev/ttyUSB0]")

if gps_device == "":
        gps_device = "/dev/ttyUSB0"

c.add_section("Settings")
c.set("Settings", "url", apiurl) #must include a trailing slash
c.set("Settings", "mongodb", mongodb)
c.set("Settings", "mongocoll_obd", mongocollection_obd)
c.set("Settings", "mongocoll_gps", mongocollection_gps)
c.set("Settings", "sqlite_gps_db", sqlite_gps_db)
c.set("Settings", "sqlite_obd_db", sqlite_obd_db)
c.set("Settings", "gps_device", gps_device)

c.write(f) #setup the URL before registering email address, so you know which server to register with.
f.close

email = raw_input("Please enter your email address: ")

if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
	print "Invalid email address. Try again."
	sys.exit(0)

print "Your email: " + email

key = jnsdk.RegisterNewUser(email)

print "Your API Key: " + key

f = open("config.txt", "w")

#c.set("Settings", "API_Key", "DEFAULTAPIKEY123")
c.set("Settings", "API_Key", key)

c.write(f)
f.close()
