

import mpu_6050_new, sys, time 


mpu = mpu_6050_new.MPU6050()

while True:
  mpu_dict = mpu.readSensors()
  mpu_str = "AX: {0:<15}, AY: {1:<15}, AZ: {2:<15}, GX: {3:<15}, GY: {4:<15}, GZ: {5:<15} \r"
  sys.stdout.write(mpu_str.format(mpu_dict['AX'], mpu_dict['AY'], mpu_dict['AZ'],
                                  mpu_dict['GX'], mpu_dict['GY'], mpu_dict['GZ']))
  sys.stdout.flush()
  time.sleep(0.5)
  
  
