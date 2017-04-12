#! /usr/bin/env python

from __future__ 	import division
from math			import cos, acos, sin, pi
from serial			import Serial
import datetime, sys


# Notes:
#
# http://aprs.gids.nl/nmea/
# https://rl.se/gprmc
#

# $GPRMC,001225,A,2832.1834,N,08101.0536,W,12,25,251211,1.2,E,A*03

class GPSpeedo():
	
	r		= 6371000
	FMT = "%H:%M:%S.%f"
		
	def __init__(self):
		coords				= {'LAT':0, 'LON':0, 'TIME':"235959.99"}
		self.start_coords	= coords
		self.stop_coords	= coords
		self.speed_ms		= 0
		self.speed_kmh		= 0
		self.distance		= 0

	
	def gps2dec(self, coord_text):
		try:
			major, minor = coord_text.split('.')	
		except:
			pass
		degrees	= int(major) // 100
		minutes	= (int(major) % 100 + float('0.' + minor)) / 60
		return degrees + minutes


	def gps_time2obj(self, time_text):
		
		major, minor	= time_text.split('.')
		hours			= int(major) // 10000
		minutes 		= (int(major) % 10000) // 100
		sec				= int(major) % 100
		ssec			= int(minor)
		time_str 		= "{0}:{1}:{2}.{3}".format(hours, minutes, sec, ssec) 
		time_obj		= datetime.datetime.strptime(time_str, self.FMT)
		
		return time_obj	
		
		
	def get_coords(self, lat, lon, time):
		self.start_coords	= self.stop_coords
		self.stop_coords	= {'LAT':self.gps2dec(lat), 'LON':self.gps2dec(lon), 'TIME':time}
		time_diff	= self.gps_time2obj(self.stop_coords['TIME'])\
					- self.gps_time2obj(self.start_coords['TIME'])
					
		self.time_diff = time_diff.seconds										
		if not self.time_diff:
			return False
		return self._calc_speed()
		
		
	def _calc_speed(self):
		
		lat1 = (self.start_coords['LAT'] * pi) / 180
		lon1 = (self.start_coords['LON'] * pi) / 180
		
		lat2 = (self.stop_coords['LAT'] * pi) / 180
		lon2 = (self.stop_coords['LON'] * pi) / 180

		rho1	= self.r * cos(lat1)
		z1		= self.r * sin(lat1)
		x1		= rho1 * cos(lon1)
		y1		= rho1 * sin(lon1)
		
		rho2	= self.r * cos(lat2)
		z2		= self.r * sin(lat2)
		x2		= rho2 * cos(lon2)
		y2		= rho2 * sin(lon2)
		
		dot			= x1 * x2 + y1 * y2 + z1 * z2
		cos_theta	= dot / (self.r ** 2)

		theta = acos(round(cos_theta, 6))

		self.distance = self.r * theta
		
		self.speed_ms	= self.distance / self.time_diff 
		self.speed_kmh	= self.speed_ms * 3.6 # 3600 / 1000  
		return (self.speed_ms, self.speed_kmh)	
		


	


speedometer = GPSpeedo()

	
rfcomm		= Serial('/dev/serial0')
rfcomm.flush()	
#f = open('speed.test', 'w')
while True:
	gps_line = rfcomm.readline()
	if 'GPGGA' in gps_line:
		
		line_split = gps_line.split(',')
		time_stamp, lat, lon = line_split[1].strip(), line_split[2].strip(), line_split[4].strip()
		
		if speedometer.get_coords(lat, lon, time_stamp):
			out_text = "{0} -> SPEED: {1:6.2f} km/h {2:6.2f} m/s\tLAT: {3} LON: {4}\tTIME: {5}".format(time_stamp, speedometer.speed_kmh, speedometer.speed_ms, lat, lon, speedometer.time_diff) 
			print out_text
		
	elif 'GPRMC' in gps_line:
		line_split = gps_line.split(',')
		time_stamp, lat, lon ,speed = line_split[1].strip(), line_split[3].strip(), line_split[5].strip(), line_split[7].strip()
		print time_stamp, lat, lon ,str(float(speed) * 1.852) + " km/h"
		
		
			
		#f.write(out_text + '\n')	 
	rfcomm.flush()	
