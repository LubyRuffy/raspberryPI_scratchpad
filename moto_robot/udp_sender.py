#! /usr/bin/env python

import socket, time
from mpu_6050 import MPU6050   
    
UDP_IP	 	= "192.168.0.11"
UDP_PORT 	= 31492
FREQ	 	= 25
__INTERVAL 	= 1/FREQ
       
mpu = MPU6050()       
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	mpu_data	= mpu.readSensors()
	MESSAGE		= "%.2f, %.2f, %.2f" % (mpu_data[3], mpu_data[4], mpu_data[5])
	print "Sending: ", MESSAGE
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	time.sleep(__INTERVAL)
