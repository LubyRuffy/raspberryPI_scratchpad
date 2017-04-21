

import mpu_6050, sys, time 


mpu = mpu_6050.MPU6050()

while True:
  sys.stdout.write(str(mpu.readSensors()) + "\r")
  time.sleep(0.1)
