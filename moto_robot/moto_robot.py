#! /usr/bin/env python

from motor_ctrl import Motor
from mpu_6050	import MPU6050
import time
from threading import Thread


class Gyro(Thread):
  def __init__(self, delay = 0.005):
    self._tilt = 0
    self.keep_running = True
    self.gyro = MPU6050()
    Thread.__init__()
  
  @property
  def tilt(self):
    return self._tilt
    
  def run():
    while keep_running:
      self._tilt	= gyro.readSensors()[1] * 90
      time.sleep(delay)


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
  while not TILT:time.sleep(DELAY)
  print "MPU6050 ready. Starting robot ..."

  try:
    while True:
      print gyro.tilt
      time.sleep(0.2)
      
  except:
    print "Stopping motors and MPU6050 ..."
    gyro.keep_running = False
    gyro.join()
    motor1.stop()
    motor1.cleanup()

    motor2.stop()
    motor2.cleanup()
    print "Robot stopped."

