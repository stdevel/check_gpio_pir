#!/usr/bin/env python

# check_gpio_pir.py - Nagios/Icinga plugin for checking
# passive infrared (PIR) sensor connected using GPIO
#
# 2014 By Christian Stankowic
# <info at stankowic hyphen development dot net>
# https://github.com/stdevel
#

import RPi.GPIO as GPIO
import time
from optparse import OptionParser

#ignore warnings
GPIO.setwarnings(False)

#use Board PIN numbers
GPIO.setmode(GPIO.BOARD)



if __name__ == "__main__":
	#define description, version and load parser
	desc='''%prog is used to check whether a PIR sensor connected using GPIO detects an amount of motions withing a time period. Detected motion can also be confirmed by a flashing LED.
	Use the parameters mentioned beyond to control the behavior of this plugin.
	
	Checkout the GitHub page for updates: https://github.com/stdevel/check_gpio_pir'''
	
	parser = OptionParser(description=desc,version="%prog version 0.1")
	
	#-d / --debug
	parser.add_option("-d", "--debug", dest="debug", default=False, action="store_true", help="enable debugging outputs (default: no)")
	
	#-l / --enable-led
	parser.add_option("-l", "--enable-led", dest="enableLED", default=False, action="store_true", help="enable LED blinking for motion detection (default: no)")
	
	#-p / --led-pin
	parser.add_option("-p", "--led-pin", dest="ledPIN", default=11, action="store", type="int", metavar="PIN", help="GPIO PIN of debug LED (default: 11)")
	
	#-i / --sensor-pin
	parser.add_option("-i", "--sensor-pin", dest="sensorPIN", default=7, action="store", type="int", metavar="PIN", help="GPIO PIN of PIR sensor (default: 7)")
	
	#-t / --seconds
	parser.add_option("-t", "--seconds", dest="seconds", default=15, action="store", type="int", help="threshold in seconds the sensor is read (default: 15)")
	
	#-c / --motion-threshold
	parser.add_option("-c", "--motion-threshold", dest="motionThreshold", default=3, action="store", type="int", metavar="COUNTER", help="threshold of motions that trigger a warning event (default: 3)")
	
	#parse arguments
	(options, args) = parser.parse_args()
	
	#show parameters
	if options.debug: print "DEBUG:",options
	
	#setup sensor
	try:
		GPIO.setup(options.sensorPIN, GPIO.IN)
	except:
		print "UNKNOWN: unable to read sensor - check GPIO PIN #"+str(options.sensorPIN)
		exit(3)
	
	#setup LED
	if options.enableLED:
		try:
			GPIO.setup(options.ledPIN, GPIO.OUT)
		except:
			print "UNKNOWN: unable to set LED - check GPIO PIN #"+str(options.ledPIN)
			exit(3)
	
	#state and counter variables
	old_state=0
	current_state=0
	checks=0
	motions=0
	
	#check sensor for motions occured in timeperiod
	while checks < options.seconds:
        	try:
			#switch LED off and read PIR state
			if options.enableLED: GPIO.output(options.ledPIN, GPIO.LOW)
			current_state = GPIO.input(options.sensorPIN)
			
			#whether the current state differs from old state
			if current_state==1 and old_state==0:
				motions = motions+1
				if options.debug: print "DEBUG: Motion detected!"
				if options.enableLED: GPIO.output(options.ledPIN, GPIO.HIGH)
				old_state=1
			elif current_state==0 and old_state==1:
				motions = motions+1
				if options.debug: print "DEBUG: Motion detected!"
				if options.enableLED: GPIO.output(options.ledPIN, GPIO.HIGH)
				old_state=0
			
			#increase counter and wait 1 second
			checks = checks+1
			if options.debug: print "DEBUG: checks done:",checks," - motions:",motions
			time.sleep(1)
        	except KeyboardInterrupt:
                	print "UNKNOWN: check terminated by keystroke"
	                GPIO.cleanup()
	                exit(3)
		except:
			print "UNKNOWN: unable to read sensor - check GPIO PIN #"+str(options.sensorPIN)
			exit(3)
	
	#checks finished - return result
	if motions >= options.motionThreshold:
		print "WARNING:",motions,"motions detected!"
		exit(1)
	else:
		print "OK: motion counter ("+str(motions)+") beyond threshold ("+str(options.motionThreshold)+")"
		exit(0)
