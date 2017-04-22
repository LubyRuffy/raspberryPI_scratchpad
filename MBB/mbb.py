#! /usr/bin/env python


from mpu_6050   import MPU6050
from gps_reader import GPSreader
from threading  import Thread

import logging, datetime, os, zipfile, time


LOG_FILE_CADENCE = 5


def zip_and_send(filename):
  print(filename) 
  zf = zipfile.ZipFile(filename + ".zip", mode = 'w') 
  zf.write(filename)
  zf.close()
  return 0
  
  
class MPU_gen(Thread):
  
  def __init__(self):
    
    self.mpu = MPU6050()
    self.mpu_dict = {'GX':[], 'GY':[], 'GZ':[]}
    Thread.__init__(self)
  
  def run(self):
    
    while True:
      mpu_dict = self.mpu.readSensors()
      self.mpu_dict['GX'].append(round(mpu_dict['GX'], 6)) 
      self.mpu_dict['GY'].append(round(mpu_dict['GY'], 6)) 
      self.mpu_dict['GZ'].append(round(mpu_dict['GZ'], 6))
      time.sleep(0.1)
      
      
  def mpu_gen(self):
    while True:
      yield self.mpu_dict
      self.mpu_dict = {'GX':[], 'GY':[], 'GZ':[]}
  


if __name__ == '__main__':
  
  logger = logging.getLogger('GPS_main_logger')
  logger.setLevel(logging.INFO)
  
  #log_path      = "{0}/bbb_logs".format(os.path.expanduser('~'))
  log_path      = "/var/log/mbb_logs"
  if not os.path.exists(log_path):
      os.mkdir(log_path)
          
  log_file      = "MBB.{0}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H:%M"))
  log_full_path = os.path.join(log_path, log_file) 
    
  file_handler  = logging.FileHandler(log_full_path)
  
  gps_log_format = logging.Formatter('%(asctime)s - %(message)s', '%Y.%m.%d-%H:%M:%S')
  file_handler.setFormatter(gps_log_format)
  
  console_handler = logging.StreamHandler()
  console_handler.setFormatter(gps_log_format)
  
  logger.addHandler(file_handler)
  logger.addHandler(console_handler)
  
  gps_message_format = "LAT:{LAT:.6f}; LON:{LON:.6f}; SPEED_GPS:{SPEED_GPS:.3f}; SPEED_CALC:{SPEED_CALC:.3f}; GPS_TIME:{TIME}"
#  mpu_message_format = "GYRO_X:{GX:.6f}; GYRO_Y:{GY:.6f}; GYRO_Y:{GZ:.6f}"
  mpu_message_format = "GYRO_X:{GX}; GYRO_Y:{GY}; GYRO_Y:{GZ}"


  gps = GPSreader('/dev/serial0')
  #mpu = MPU6050()
  mpu = MPU_gen()

#  try:
#    mpu.readOffsets('mpu.conf')
#  except:
#    pass    

  start_time = datetime.datetime.now()
  #mpu.start()
  for coords in gps.coords:
    #mpu_data = mpu.mpu_gen()
#    try:  
#      mpu_data = mpu.readSensors()
#    except:
#      mpu_data = {'GX':0, 'GY':0, 'GZ':0, 'AX':0, 'AY':0, 'AZ':0} 
      
    curr_time = datetime.datetime.now()
    if (curr_time.second == 0 or curr_time.second < start_time.second)\
        and abs(curr_time.minute - start_time.minute) % 10 == LOG_FILE_CADENCE:
      
      ### Logs rotation section    
      old_log_full_path = log_full_path
      log_file          = "BBB.{0}.log".format(datetime.datetime.now().strftime("%Y%m%d_%H:%M"))
      log_full_path     = os.path.join(log_path, log_file) 
      
      logger.removeHandler(file_handler)      
      file_handler  = logging.FileHandler(log_full_path)
      file_handler.setFormatter(gps_log_format)
      logger.addHandler(file_handler)
      
      start_time = datetime.datetime.now()
      ### End of log rotation section 
    
      Thread(target = zip_and_send, args = (old_log_full_path,)).start() 
    
    gps_message = gps_message_format.format(**coords)
    #mpu_message = mpu_message_format.format(**mpu_data)
    logger.info(gps_message)# + "; " + mpu_message)
