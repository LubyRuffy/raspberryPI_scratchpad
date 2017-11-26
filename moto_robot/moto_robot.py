#! /usr/bin/env python

from __future__ import division

import time

from threading import Thread
from mpu_6050	import MPU6050
from motor_ctrl import Motor

WHEEL_SPEED = 0.3


class Gyro(Thread):
  def __init__(self, delay = 0.005):
    self._tilt = 0
    self.__delay = delay
    self.keep_running = True
    self.__mpu6050 = MPU6050()
    Thread.__init__(self)
  
  @property
  def tilt(self):
    return self._tilt
    
  def run(self):
    while self.keep_running:
      self._tilt = self.__mpu6050.readSensors()[1] * 90
      time.sleep(self.__delay)


def goLeft(mspeed, delay):
  motor1.go_left(mspeed)
  motor2.go_left(mspeed)
  time.sleep(speed)

def goRight(mspeed, delay):
  motor1.go_right(mspeed)
  motor2.go_right(mspeed)
  time.sleep(delay)
  
  
def stopMotors(delay):
  motor1.stop()
  motor2.stop()
  time.sleep(delay)


if __name__ == "__main__":

  motor1	= Motor(13, 15, 100)
  motor2	= Motor(16, 18, 100)

  gyro  = Gyro()

  print "Initializing MPU6050 ..."
  gyro.start()	
  while not gyro.tilt:
    time.sleep(0.2)
  print "MPU6050 ready. Starting robot ..."

  while True:
    tilt = gyro.tilt
    delay = (abs(tilt) / 360) * WHEEL_SPEED
    if tilt > 0:
      goLeft(100, delay)
    elif tilt < 0:
      goRight(100, delay)
    
    #stopMotors(0)
        
  print "Stopping motors and MPU6050 ..."
  gyro.keep_running = False
  gyro.join()
  motor1.stop()
  motor1.cleanup()

  motor2.stop()
  motor2.cleanup()
  print "Robot stopped."

