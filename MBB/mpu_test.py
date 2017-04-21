

import mpu_6050, sys 


mpu = MPU6050()

while True:
  sys.stdout.write(str(mpu.readSensors()) + "\r")
   
