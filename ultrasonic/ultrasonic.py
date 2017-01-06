#! /usr/bin/env python

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


TRIG = 23
ECHO = 24

SOUND_SPEED = 34000 #Old: 17150
 
print "Distance Measurement In Progress"
 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
 
GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)
 
GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

try:
	
	while True:		
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		
		while GPIO.input(ECHO)==0:
			pulse_start = time.time()
		 
		while GPIO.input(ECHO)==1:
			pulse_end = time.time()
		 		 
		pulse_duration = pulse_end - pulse_start
		distance = round(pulse_duration * 17150)
		 
		print "Distance:",distance,"cm"
		time.sleep(0.1)
		
except KeyboardInterrupt:
	GPIO.cleanup()

