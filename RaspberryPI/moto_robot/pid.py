#! /usr/bin/env python


class PID:
	
    def __init__(self, kp = 0, ki = 0, kd = 0):
		
		self.kp			= kp
		self.ki			= ki
		self.kd			= kd
		self.error 		= 0
		self.last_error = self.error

    def update(self, angle, acceleration, delay):
		
		angle			/= 10
		acceleration	/= 10
		
		self.error = angle + (acceleration * delay)
		
		pTerm			= self.error * self.kp
		iTerm			= self.error * self.ki
		dTerm			= (self.error - self.last_error) * self.kd
		self.last_error = self.error
			
		return pTerm + iTerm + dTerm
		
		
		
		
if __name__ == "__main__":
			
    pid = PID(kp=30, ki=10, kd=10)

    print pid.update(10, 40, 0.2)
    print pid.update(5, 20, 0.2)
    print pid.update(-5, -20, 0.2)

