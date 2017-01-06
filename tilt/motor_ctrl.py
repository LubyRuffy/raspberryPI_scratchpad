#! /usr/bin/env python

import RPi.GPIO as gpio

class Motor:
	
	def __init__(self, pin1, pin2, freq):
		
		self.in1	= pin1
		self.in2	= pin2
		
		self.RIGHT		= False
		self.LEFT		= False
		self.STOPPED	= False
		
		if 	gpio.getmode() != gpio.BOARD:			
			gpio.setmode(gpio.BOARD)
			
		gpio.setup(self.in1, gpio.OUT)
		gpio.setup(self.in2, gpio.OUT)
		
		self.pwm_out1 = gpio.PWM(self.in1, freq)
		self.pwm_out2 = gpio.PWM(self.in2, freq)
		self.pwm_out1.start(0)
		self.pwm_out2.start(0)
		
		
	def go_right(self, speed):
		self.pwm_out1.ChangeDutyCycle(0)
		self.pwm_out2.ChangeDutyCycle(speed)
		self.RIGHT, self.LEFT = True, False
		self.STOPPED = False		


	def go_left(self, speed):
		self.pwm_out1.ChangeDutyCycle(speed)
		self.pwm_out2.ChangeDutyCycle(0)
		self.LEFT, self.RIGHT = True, False
		self.STOPPED = False


	def stop(self):
		self.pwm_out1.ChangeDutyCycle(0)
		self.pwm_out2.ChangeDutyCycle(0)
		self.LEFT, self.RIGHT = False, False
		self.STOPPED = True

        
	def cleanup(self):
		self.pwm_out1.stop()
		self.pwm_out2.stop()
		gpio.cleanup(self.in1)
		gpio.cleanup(self.in2)	


if __name__ == "__main__":
	pass
	
