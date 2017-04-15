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
  
  message_format = "LAT:{LAT}; LON:{LON}; SPEED:{SPEED}; GPS_TIME:{TIME}"  
  gps = GPSreader('/dev/serial0')
  
  start_time = datetime.datetime.now()
  for coords in gps.coords:
    logger.info(message_format.format(**coords)) 
    
    curr_time = datetime.datetime.now()
    if curr_time.second == 0 and abs(curr_time.minute - start_time.minute) % 10 == LOG_FILE_CADENCE:
      log_file      = "BBB.{0}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H:%M"))
      log_full_path = os.path.join(log_path, log_file) 
      file_handler  = logging.FileHandler(log_full_path)
      logger.addHandler(file_handler)
      start_time = datetime.datetime.now()  
