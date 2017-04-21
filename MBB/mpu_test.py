

import mpu_6050, sys, time 


mpu = mpu_6050.MPU6050()

while True:
  mpu_dict = mpu.readSensors()
  mpu_str = "AX: {:<0}, AY: {:<1}, AZ: {:<2}, GX: {:<3}, GY: {:<4}, GZ: {:<5} \r"
  sys.stdout.write(mpu_str.format(mpu_dict['AX'], mpu_dict['AY'], mpu_dict['AZ'],
                                  mpu_dict['GX'], mpu_dict['GY'], mpu_dict['GZ']))
  sys.stdout.flush()
  time.sleep(0.1)
  
  
