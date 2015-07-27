#!/usr/bin/env python
import os, sys, Adafruit_DHT, time, json, math, requests, pickle, logging, spidev
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
from uuid import getnode as get_mac
from collections import defaultdict

##################################################
##############Variables###########################
global data, dataDay, todayDate
sensor                       = Adafruit_DHT.AM2302 #DHT11/DHT22/AM2302
pin                          = 4
home	                     = "/home/pi/projects/humTempScript/"
measureFilePath		     = home + "sensorValues/"
sec_between_log_entries      = 900
url			     = "your URL"
headers		   	     = {'Content-type': 'application/json', 'Accept': 'text/plain'}
myhost			     = os.uname()[1]
uid			     = myhost + "@gmail.com"
dateformat		     = "%4d-%02d-%02d-%02d-%02d-%02d"
data			     = [ ] #data is sent to the server as json
dataDay			     = [ ] #dataDay is dumped on the log file
macFormat		     =  "{0:x}"
todayDate		     = None;
global d
d			     = defaultdict(int)
d			     = {}

#use spidev to open the serial port

spi = spidev.SpiDev()
spi.open(0,0)

##################################################
##############Function to read MCP################
#def getAdc(sensorChannel0):
def getAdc():
	global d
	d = {}
	for x in range(0, 8):
		sensorAsk =  spi.xfer2([1, (8+x) << 4, 0])
		sensorRead = ((sensorAsk[1]&3) << 8) + sensorAsk[2]
		d['sensor%01d' % x]= sensorRead


##################################################
##############Get Mac Address#####################
mac = get_mac()
mac = macFormat.format(mac)


##################################################
##############Functions ##########################

###### Today Date ######
def setTodayDate():
    global todayDate;
    todayDate = datetime.now().day
 

###### CHECK DATE ######
def isChangeDate():
    global todayDate;
    if(todayDate != datetime.now().day):
        return True;
    return False;


###### ERASE DATA ######
def eraseData():
    global todayDate, dataDay;
    if(isChangeDate()) or len(str(dataDay)) >= 562000:
        setTodayDate();
        dataDay = [ ]


##################################################
############Create a log file per day#############
#stores the file in home + measureFilePath
#most likely /home/piprojects/humTempScript/Measurements

def writeToFile():
	global todayDate, dataDay;
	monthDayDate = time.strftime("%d-%m-%Y")
	fileLog = measureFilePath + myhost + "-" + monthDayDate + "-RHT-measures"
	with open(fileLog, 'wb') as f:
		pickle.dump(dataDay, f)
	eraseData()
#to get to written data do : pp = pickle.load(open(measureFilePath + todayDate + "-RHT-measures", "rb"))


##################################################
###### SEND Json TIMER ###########################
#Call back function by the scheduler
def jsonSend_callback():
	send_json()


##################################################
###### SEND Json  ################################
#POST data as Json on url
def send_json():
	global data
	r = requests.post(url, data=json.dumps(data), headers=headers)
	if str(r) == "<Response [200]>" or len(str(data)) >= 562000:
		data = [ ]

##################################################
###### ADD Data ##################################
#add data set to Json
def add_DataSet(UID, mac, date, temperature, humidity, soil):
	global data
	global dataDay
	data.append({"UID":UID, "MAC":mac, "date":date, "temperature":temperature, "humidity":humidity, "soilMoisture":soil})
	dataDay.append({"UID":UID, "MAC":mac, "date":date, "temperature":temperature, "humidity":humidity, "soilMoisture":soil})


##################################################
###### Ignore first 10 measures###################
#print "Ignoring first 10 sensors values to improve quality..."
for x in range(10):
	Adafruit_DHT.read_retry(sensor, pin)


##################################################
###### Creating interval timer ###################
#print "Creating interval timer. Wait a bit..."
scheduler = BackgroundScheduler()
scheduler.add_job(writeToFile, 'interval', seconds=sec_between_log_entries)
scheduler.add_job(jsonSend_callback, 'interval', seconds=sec_between_log_entries)
scheduler.start()
#print "Started interval timer which will be called the first time in {0} seconds.".format(sec_between_log_entries);


##################################################
######### Get today's date #######################
setTodayDate()
logging.basicConfig()
try:
	while True:
		hum, temp = Adafruit_DHT.read_retry(sensor, pin)
		getAdc()
		current_time = time.localtime()[0:6]
		date = dateformat % current_time[0:6]
		soil = str(int(100-round(d['sensor0']/10.24)))
		temp = str(round(temp, 1))
		hum = str(round(hum, 1))
		add_DataSet(uid, mac, date, temp, hum, soil)
		time.sleep(60)
except (KeyboardInterrupt, SystemExit):
	scheduler.shutdown()
