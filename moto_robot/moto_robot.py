#! /usr/bin/env python

from motor_ctrl import Motor
from mpu_6050	import MPU6050
import time
from threading import Thread

DELAY		= 0.005
HYST_START	= 1
HYST_STOP	= 5
SPEED           = 50

TILT	= None
RUN	= True 


def getTilt():
	global TILT
	gyro	= MPU6050()
	while RUN:
		TILT	= gyro.readSensors()[1] * 90
		time.sleep(DELAY)


def goLeft():
	while RUN:	
		if TILT < (HYST_START * -1):
			while TILT < (HYST_STOP * -1) and RUN:
				motor1.go_left(SPEED)
				motor2.go_left(SPEED)
				time.sleep(DELAY)
				
			
def goRight():	
	while RUN:
		if TILT > HYST_START:
			while TILT > HYST_STOP and RUN:
				motor1.go_right(SPEED)
				motor2.go_right(SPEED)
				time.sleep(DELAY)
			
				
def stopMotors():
	while RUN:
		if TILT < HYST_STOP and (TILT > HYST_STOP * -1):
			motor1.stop()
			motor2.stop()
			time.sleep(DELAY)		



if __name__ == "__main__":
	
	motor1	= Motor(13, 15, 100)
	motor2	= Motor(16, 18, 100)
	
	gyro_thread 	= Thread(target = getTilt)
	go_right_thread	= Thread(target = goRight)
	go_left_thread	= Thread(target = goLeft)
	stop_motors     = Thread(target = stopMotors)
	
	print "Initializing MPU6050 ..."
	gyro_thread.start()	
	while not TILT:time.sleep(DELAY)
	print "MPU6050 ready. Starting robot ..."

	go_left_thread.start()
	go_right_thread.start()
	stop_motors.start()	
	
	try:
		while True:time.sleep(1)
	except:
		print "Stopping motors and MPU6050 ..."
		RUN = False
		gyro_thread.join()	
		go_left_thread.join()
		go_right_thread.join()
		stop_motors.join()	
			
		motor1.stop()
		motor1.cleanup()
		
		motor2.stop()
		motor2.cleanup()
		print "Robot stopped."

