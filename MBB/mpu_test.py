

import mpu_6050, sys, time 


mpu = mpu_6050.MPU6050()

while True:
  mpu_dict = mpu.readSensors()
  sys.stdout.write(mpu_dict['GX'] + "\r")
  time.sleep(0.1)
  sys.stdout.flush()
