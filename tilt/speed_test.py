#! /usr/bin/env python


from mpu_6050	import MPU6050
from motor_ctrl import Motor
from threading	import Thread
from pid		import PID

import time


MAX_TILT	= 15
FREQ		= 50
MIN_SPEED	= 30
MAX_SPEED	= 100
DELAY		= 0.02
HYSTERESIS	= 2
TILT		= None
RUN			= True


def getTilt():
	global TILT
	gyro	= MPU6050()
	pid     = PID(kp = 10)
	while RUN:
                start_time  = time.time()
		gyro_data   = gyro.readSensors()
                tilt        = gyro_data[1] * 90
                acc         = gyro_data[3]
                run_time = time.time() - start_time
                if run_time < DELAY:
                    time.sleep(DELAY - run_time)
                    TILT    = int(tilt + (acc * DELAY))
                    print pid.update(tilt, acc, DELAY)
                else:
                    TILT    = int(tilt + (acc * run_time))
                    print pid.update(tilt, acc, run_time)


if __name__ == "__main__":
	
	motor1		= Motor(13, 15, FREQ)
	motor2		= Motor(16, 18, FREQ)
	gyro_thread = Thread(target = getTilt)
	
	print "Initializing MPU6050 ..."
	gyro_thread.start()	
	while not TILT:time.sleep(DELAY)
	print "MPU6050 ready. Starting robot ..."
		
	speeds = map(lambda s: int((((MAX_SPEED - MIN_SPEED)/float(MAX_TILT)) *  s) + MIN_SPEED), range(MAX_TILT + 1))
	print speeds
	try:		
	    while True:
	        spd_idx = abs(TILT//2) - HYSTERESIS if abs(TILT//2) <= (MAX_TILT + HYSTERESIS) and abs(TILT//2) >= HYSTERESIS else MAX_TILT 
	        spd 	= speeds[spd_idx]
		if TILT > HYSTERESIS:	
			motor1.go_right(spd)
			motor2.go_right(spd)
		elif TILT < -HYSTERESIS:
			motor1.go_left(spd)
			motor2.go_left(spd)
		else:
			motor1.stop()
			motor2.stop()

		time.sleep(DELAY)
	except:
            RUN = False
            gyro_thread.join()
	    motor1.cleanup()	
	    motor2.cleanup()	


