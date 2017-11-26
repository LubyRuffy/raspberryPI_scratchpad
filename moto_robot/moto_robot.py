#! /usr/bin/env python

from __future__ import division

import sys
import time

from threading import Thread
from mpu_6050	import MPU6050
from motor_ctrl import Motor

WHEEL_SPEED = 0.3


class Gyro(Thread):
  def __init__(self, delay = 0.01):
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
  time.sleep(delay)

def goRight(mspeed, delay):
  motor1.go_right(mspeed)
  motor2.go_right(mspeed)
  time.sleep(delay)
  
  
def stopMotors(delay):
  motor1.stop()
  motor2.stop()
  time.sleep(delay)


if __name__ == "__main__":

  try:
    speed = int(sys.argv[1])
  except Exception:
    print "Motor speed needed."
    sys.exit(-1)

  wheel_speed = (WHEEL_SPEED / speed) * 100

  motor1	= Motor(13, 15, 100)
  motor2	= Motor(16, 18, 100)

  gyro  = Gyro()

  print "Initializing MPU6050 ..."
  gyro.start()	
  while not gyro.tilt:
    time.sleep(0.2)
  print "MPU6050 ready. Starting robot ..."

  try:
    while True:
      #comment
      tilt = gyro.tilt
      delay = ((abs(tilt) / 360) * wheel_speed) / 2 
      print delay
      if tilt < 0:
        goLeft(speed, delay)
      elif tilt > 0:
        goRight(speed, delay)

  except KeyboardInterrupt:
    print "Stopping motors and MPU6050 ..."
    gyro.keep_running = False
    gyro.join()
    motor1.stop()
    motor1.cleanup()

    motor2.stop()
    motor2.cleanup()
    print "Robot stopped."
