#! /usr/bin/env python


from mpu_6050	import MPU6050
from threading	import Thread
import time, sys


MAX_TILT	= 30
FREQ		= 50
MIN_SPEED	= 30
MAX_SPEED	= 100
DELAY		= 0.1
HYSTERESIS	= 2
TILT		= None
ACCELERATION	= None
RUN             = True


def getTilt():
	global TILT
	global ACCELERATION
	gyro	= MPU6050()
	while RUN:
		gyro_data	= gyro.readSensors()
		TILT 		= gyro_data[1]
		ACCELERATION	= gyro_data[3]
		time.sleep(DELAY)


if __name__ == "__main__":
	
    gyro_thread = Thread(target = getTilt)
	
    print "Initializing MPU6050 ..."
    gyro_thread.start()	
    while not TILT:time.sleep(DELAY)
    print "MPU6050 ready. Starting robot ..."
    try:	
        while True:
            print TILT, ACCELERATION
            time.sleep(DELAY)
    except:
        RUN = False
        gyro_thread.join()
        sys.exit(0)


