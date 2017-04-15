#! /usr/bin/env python


#from mpu_6050   import MPU6050
from gps_reader import GPSreader

import logging, datetime, os


LOG_FILE_CADENCE = 2

if __name__ == '__main__':
  
  logger = logging.getLogger('GPS_main_logger')
  logger.setLevel(logging.INFO)
  
  log_path      = "{0}/bbb_logs".format(os.path.expanduser('~'))
  log_file      = "BBB.{0}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H:%M"))
  log_full_path = os.path.join(log_path, log_file) 
    
  file_handler  = logging.FileHandler(log_full_path)
  
  gps_log_format = logging.Formatter('%(asctime)s - %(message)s', '%Y.%m.%d-%H:%M:%S')
  file_handler.setFormatter(gps_log_format)
  
  console_handler = logging.StreamHandler()
  console_handler.setFormatter(gps_log_format)
  
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
  
  gps_message_format = "LAT:{LAT}; LON:{LON}; SPEED:{SPEED}; GPS_TIME:{TIME}"
  mpu_message_format = "GYRO_X:{GX}; GYRO_Y:{GX}; GYRO_Z:{GZ}; ACCEL_X:{AX}; ACCEL_Y:{AY}; ACCEL_Z:{AZ}; TEMP:{TEMP}"
  gps = GPSreader('/dev/serial0')
  
  start_time = datetime.datetime.now()
  for coords in gps.coords:
    gps_message = gps_message_format.format(**coords)
    logger.info(gps_message) 
    
    curr_time = datetime.datetime.now()
    if (curr_time.second == 0 or curr_time.second < start_time.second)\
        and abs(curr_time.minute - start_time.minute) % 10 == LOG_FILE_CADENCE:
      
      log_file      = "BBB.{0}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H:%M"))
      log_full_path = os.path.join(log_path, log_file) 
      logger.removeHandler(file_handler)      
      file_handler  = logging.FileHandler(log_full_path)
      file_handler.setFormatter(gps_log_format)
      logger.addHandler(file_handler)
      
      start_time = datetime.datetime.now()  
