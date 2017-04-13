#! /usr/bin/env python


from mpu_6050	import MPU6050
from motor_ctrl import Motor
from threading	import Thread
from pid        import PID

import time


MAX_TILT	= 15
FREQ		= 50
MIN_SPEED	= 30
MAX_SPEED	= 100
DELAY		= 0.02
TILT		= None
ACC             = None
RUN             = True


def getTilt():
	global TILT
        global ACC
	gyro	= MPU6050()
	while RUN:
                start_time  = time.time()
		gyro_data   = gyro.readSensors()
                TILT        = gyro_data[1] * 90
                ACC         = gyro_data[3]
                run_time = time.time() - start_time
                if run_time < DELAY:
                    time.sleep(DELAY - run_time)


if __name__ == "__main__":
	
	motor1		= Motor(13, 15, FREQ)
	motor2		= Motor(16, 18, FREQ)
	gyro_thread = Thread(target = getTilt)
	
	print "Initializing MPU6050 ..."
	gyro_thread.start()	
	while not TILT and not ACC:time.sleep(DELAY)
	print "MPU6050 ready. Starting robot ..."
        pid = PID(kp = 50, ki=0, kd=0)
		
	try:		
            while True:
                spd = pid.update(TILT, ACC, DELAY)
	        if spd > 0:	
		    motor1.go_right(spd)
		    motor2.go_right(spd)
                elif spd < 0:
		    motor1.go_left(abs(spd))
		    motor2.go_left(abs(spd))

	    time.sleep(DELAY)
	except:
            RUN = False
            gyro_thread.join()
	    motor1.cleanup()	
	    motor2.cleanup()	


