# MonitoringSystemForRpi
Environmental monitoring system scalable using Digital and analog sensors - Full distro soon.

This project is a enviromental monitoring system using digital and analogs sensors.

It's composed of:

-Raspberry pi A+ (preferably) or B+ (but the distro has not been tested on B+).

-USB dongle (TP-Link: TL-WN823N)

-Digital Humity and Temperature Sensor - DHT AM3202 

-Analog to Digital Converter - MPC3008

-Resistive soil Sensor

-Analog Temperature sensor LM35

-add up to 5 more analogic sensors onf the MPC3008.


This repository will try to guide you throught the full installation of the System, OS settings included.
A full distro will be availlable soon to (september 2015).

Functionment:

A deamon runs the application to collect the measurements every minute of all sensors.
The data is sent as a Json string to a google API engine server (or whatever server). The server part is not described here.

The System also copies once a day all the measurements to a secondary server.
A remote connection is set up from the secondary server and allows full access to the System.


General configs:

Application:
The measurment application is a python script, with the following librairies:
- Adafruit_DHT
- spydev
- pickle
- apscheduler
It's run by the root user.

A script run throughta cron permit to take a picture with the Picamera and raspsistill.
By default, it take 3 pictures a day and uploads them to the secondary server.

The logging system needs a ssh key set as the logs are connected via SCP.
The remote connection is done via a reverse ssh tunnel to the RPi from the secondary server.
The previous scripts are run by the pi user.

OS:

At start up a VNC server is started.
A start up a ssh-agent is started with your key loaded with ssh-add and an expect script to allow none interactive ssh connections.

The OS settings provide a pre configured WIFI network that can be created by an Android phone hotspot.
This permit to access the Rpi throught your phone (or from your computer connected to the hotspot of your phone) via ssh or Vnc.
This way you can configure other wifi settings an access internet. This is particulary handy for the RPI A+ that has only 1 usb port.


Credits and references:

http://www.home-automation-community.com/temperature-and-humidity-from-am2302-dht22-sensor-displayed-as-chart/

http://www.instructables.com/id/Raspberry-Pi-Temperature-Humidity-Network-Monitor/

https://github.com/jervine/rpi-temp-humid-monitor

https://plot.ly/raspberry-pi/tmp36-temperature-tutorial/

http://www.instructables.com/id/Soil-Moisture-Sensor-1/?ALLSTEPS

http://www.home-automation-community.com/temperature-and-humidity-from-am2302-dht22-sensor-displayed-as-chart/

http://www.raspberrypi-spy.co.uk/2014/08/enabling-the-spi-interface-on-the-raspberry-pi/

https://github.com/Gadgetoid/py-spidev

http://pi.gadgetoid.com/pinout

https://www.raspberrypi.org/forums/viewtopic.php?f=32&t=110222&p=788582#p788582



