#!/usr/bin/env python

# This script defines how the low level hardware of the IOT BBQ works
# It is automatically restarted by systemd if it dies, so we need to 
# make sure we put the system in a safe state on startup

import RPi.GPIO as GPIO

HEATER_PIN = 18

# set mode to bcm numbering
GPIO.setmode(GPIO.BCM)

# set the pin to be a gpio input
# THIS LINE IS IMPORTANT, BECAUSE IT MAKES SURE THE DAEMON RESTARTS
# IN A SAFE STATE!!!
GPIO.setup(HEATER_PIN, GPIO.IN)

# Phew... Now that we have that out of the way, we can start the real startup process of the daemon..

import sys
import signal
import yoctopuce.yocto_api as ya
import yoctopuce.yocto_temperature as yt
import time

def shutdown_daemon(signum, frame):
    print("Received SIGTERM. Shutting down gracefully.")

    # set the gpio pin to be an input
    GPIO.setup(HEATER_PIN, GPIO.IN)
    sys.exit(0)

def init_thermocouples():
    errmsg=ya.YRefParam()

    # Setup the API to use local USB devices
    if ya.YAPI.RegisterHub("usb", errmsg)!= ya.YAPI.SUCCESS:
        sys.exit("init error"+errmsg.value)

    # get the  first sensor
    sensor = yt.YTemperature.FirstTemperature()

    if sensor is None :
        sys.exit('No module connected')

    if not(sensor.isOnline()):
        sys.exit('device not connected')

    # retrieve module serial
    serial = sensor.get_module().get_serialNumber()

    # retreive both channels
    channel1 = yt.YTemperature.FindTemperature(serial + '.temperature1')
    channel2 = yt.YTemperature.FindTemperature(serial + '.temperature2')
    return (channel1.get_currentValue, channel2.get_currentValue)    


# register the signal handler for termination of the daemon    
signal.signal(signal.SIGTERM, shutdown_daemon)

# get the thermocouples
(temp1,temp2) = init_thermocouples()

# set the heater pin to be an output
GPIO.setup(HEATER_PIN, GPIO.OUT, initial=GPIO.LOW)

print('Finished Initialization. Entering Polling Loop.')

# process sleeps here until we do something useful
while True:

    # print out temperature readings
    print('{}\t{}'.format(temp1(), temp2()))

    newval = not GPIO.input(HEATER_PIN)

    print('Setting pin to {}'.format(newval))
    
    # toggle the gpio pin
    GPIO.output(HEATER_PIN, newval)
    
    time.sleep(1)
