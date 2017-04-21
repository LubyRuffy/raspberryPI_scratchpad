#! /usr/bin/env python

from __future__   import division
from serial       import Serial
from math         import cos, acos, sin, pi

import datetime


# Notes:
#
# http://aprs.gids.nl/nmea/
# https://rl.se/gprmc
#

class GPSreader():
  
  __KNOT  = 1.852
  __r     = 6371000

  _GPRMC_pattern  = { 'HOUR':1, 'STATUS':2, 'LAT':3, 'LAT_NS':4, 'LON':5, 'LON_EW':6, 'SPEED':7,
                      'COURSE':8, 'DATE':9,  'VAR':10, 'VAR_E_W':11, 'CHKS':12, 'LENGTH':13}
  
      
  def __init__(self, port = None):
    
    if port:
      self.gps    = Serial(port)
      self.coords = self._coords_gen()
    else:
      self.get_coords = None
        
    self._speed           = 0
    self._speed_calc      = 0
    self._latitude        = 0
    self._longitude       = 0
    self._latitude_prev   = 0
    self._longitude_prev  = 0
    
    self._time_now        = 0
    self._time_prev       = 0
    
    self._timestamp   = ""
    self._gps_raw     = {}
    
  
  @property
  def speed(self):
    return round(self._speed, 3)
    
  
  @property  
  def latitude(self):
    return round(self._latitude, 7)
    
  
  @property
  def longitude(self):
    return round(self._longitude, 7)

    
  @property
  def timestamp(self):
    return self._timestamp
  
  
  def _split_gps_str(self, gps_str):
    
    self._gps_raw = {key:"" for key in self._GPRMC_pattern}
    gps_split = gps_str.split(',')
    
    if len(gps_split) == self._GPRMC_pattern['LENGTH']:
      self._gps_raw = {key:(gps_split[self._GPRMC_pattern[key]] if key != 'LENGTH' else 0) for key in self._GPRMC_pattern}
      self._gps_raw.pop('LENGTH')
    
    return self._gps_raw
      

  def _gps2coords(self, coord_text, nswe):
    
    try:
      major, minor  = coord_text.split('.')  
      degrees       = int(major) // 100
      minutes       = (int(major) % 100 + float('0.' + minor)) / 60
      coordinate    = round(degrees + minutes, 7)
      if nswe.upper() == 'W':
        return  coordinate * -1
      else:
        return coordinate
    except:
      return -1
          

  def _gps2time(self, hour_time, day_time):

    try:
      major, minor  = hour_time.split('.')
      hours         = int(major) // 10000
      minutes       = (int(major) % 10000) // 100
      sec           = int(major) % 100
      ssec          = int(minor)
      
      day           = int(day_time) // 10000
      month         = (int(day_time) % 10000) // 100 
      year          = (int(day_time) % 100) + 2000
    
      time_obj      = datetime.datetime(year, month, day, hours, minutes, sec, ssec) 
      
      return str(time_obj)
    except:
      return -1
    
    
  def _gps2speed(self, speed):
    
    try:
      self._speed = float(speed) * self.__KNOT 
      return self._speed
    except:
      return -1
      
      
  def _calc_speed(self):

		lat1 = (self._latitude_prev   * pi) / 180
		lon1 = (self._longitude_prev  * pi) / 180
		
		lat2 = (self._latitude  * pi) / 180
		lon2 = (self._longitude * pi) / 180

		rho1	= self.__r * cos(lat1)
		z1		= self.__r * sin(lat1)
		x1		= rho1 * cos(lon1)
		y1		= rho1 * sin(lon1)
		
		rho2	= self.__r * cos(lat2)
		z2		= self.__r * sin(lat2)
		x2		= rho2 * cos(lon2)
		y2		= rho2 * sin(lon2)
		
		dot			= x1 * x2 + y1 * y2 + z1 * z2
		cos_theta	= dot / (self.__r ** 2)

		theta = acos(round(cos_theta, 6))

		distance = self.__r * theta
		
		speed_calc	= (distance / (self._time_prev - self._time_now)) * 3.6 
		
		return speed_calc
      
          
  def get_coords(self, gps_str):
    
    coords_dict = {'LAT':0, 'LON':0, 'SPEED_GPS':0, 'SPEED_CALC':0, 'TIME':""}
    
    self._split_gps_str(gps_str)
    if self._gps_raw['STATUS'] == 'A':
      
      self._time_now    = time.time()
      self._latitude    = self._gps2coords(self._gps_raw['LAT'], self._gps_raw['LAT_NS'])
      self._longitude   = self._gps2coords(self._gps_raw['LON'], self._gps_raw['LON_EW'])
      self._speed       = self._gps2speed(self._gps_raw['SPEED'])
      self._timestamp   = self._gps2time(self._gps_raw['HOUR'], self._gps_raw['DATE'])
      self._speed_calc  = self._calc_speed()
      
      self._latitude_prev, self._longitude_prev = self._latitude, self._longitude
      self._time_prev = self._time_now
      
      coords_dict     = { 'LAT':self.latitude,    'LON':self.longitude,
                          'SPEED_GPS':self.speed, 'SPEED_CALC':self._speed_calc,
                          'TIME':self.timestamp}
      
    return coords_dict
    
  
  def _coords_gen(self):
    self.gps.flush()
    while True:
      gps_line = self.gps.readline()
      if "GPRMC" in gps_line:  
        yield self.get_coords(gps_line)
      
    



if __name__ == '__main__':
  
  gps_reader = GPSreader('/dev/serial0')
  for coords in gps_reader.coords:
    print(coords)
 
 
