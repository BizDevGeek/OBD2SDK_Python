import random
import time
import gps

while True:
	time.sleep(1)
	report = {}

	try:
		session = gps.gps("localhost", "2947")
		session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
		report = session.next()
	except:
		#continue along, the defaults are below.
		#continue
		time.sleep(1)

	gpstime = "Missing: Time"
	lon = "Missing: Lon"
	lat = "Missing: Lat"

	if report:
		if report['class'] == 'TPV':
			if hasattr(report, 'time'):
				#print "Time: " + str(report.time)
				gpstime = str(report.time)
			if hasattr(report, 'lon'):
				#print "Lon: " + str(report.lon)
				lon = str(report.lon)
			if hasattr(report, 'lat'):
				#print "Lat: " + str(report.lat)
				lat = str(report.lat)

	f = open('test.txt', 'a')
	#r = random.randrange(10,99)
	f.write(gpstime+"\t"+lon+"\t"+lat+"\n")
	f.close()

