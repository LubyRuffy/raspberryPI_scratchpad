#! /usr/bin/env python


#from mpu_6050   import MPU6050
from gps_reader import GPSreader

import logging, datetime


if __name__ == '__main__':
  
  logger = logging.getLogger('GPS_main_logger')
  logger.setLevel(logging.INFO)
  
  log_filename  = "BBB.{0}.log".format(datetime.datetime.now().strftime("%Y%m%d"))
  file_handler       = logging.FileHandler(log_filename)
  
  gps_log_format = logging.Formatter('%(asctime)s - %(message)s', '%Y.%m.%d-%H:%M:%S')
  file_handler.setFormatter(gps_log_format)
  
  console_handler = logging.StreamHandler()
  console_handler.setLevel(logging.INFO)
  console_handler.setFormatter(gps_log_format)
  
  
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
  
  
  message_format = "LAT:{LAT}; LON:{LON}; SPEED:{SPEED}; GPS_TIME:{TIME}"
  
  gps = GPSreader('/dev/serial0')
  for coord in gps.coords:
    logger.info(message_format.format(**coords)) 
  
  




