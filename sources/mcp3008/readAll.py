#! /usr/bin/env python

#Python programme to communicate with an MCP3008

#Import spidev wrapper and sleep function

import spidev
from time import sleep
from collections import defaultdict

#Establish SPI device on Bus 0, Device 0

spi = spidev.SpiDev()
spi.open(0,0)

global d
d = defaultdict(int)
d = {}


##################################################
##############Function to read MCP################
#def getAdc(sensorChannel0; sensorChannel1):
def getAdc():
	global d
	d = {}
	for x in range(0, 8):
		sensorAsk =  spi.xfer2([1, (8+x) << 4, 0])
		sensorRead = ((sensorAsk[1]&3) << 8) + sensorAsk[2]
		d['sensor%01d' % x]= sensorRead

while True:
	getAdc()
	sensor0 = d['sensor0']	
	sensor1 = d['sensor1']
	sensor2 = d['sensor2']
	soil = str(int(100-round(d['sensor0']/10.24)))
	soil1 = str(int(100-round(d['sensor1']/10.24)))
	soil2 = str(int(100-round(d['sensor2']/10.24)))
	print "soil " + soil + "soil1 " + soil1 + "soil2 " + soil2
	sleep(10)
