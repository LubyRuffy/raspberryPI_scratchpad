#! /usr/bin/env python




def cpu_load(interval):
	
	from time import sleep
	def get_cpu_time():
		CPUs_time = []
		stat_out = open("/proc/stat","r").readlines()
		for line in stat_out:
			if "cpu" in line:
				cpu_total_time	= 0
				cpu_idle_time	= 0
				for field in line.split():
					try:
						cpu_total_time += float(field)
					except:
						pass
					
				cpu_idle_time = float(line.split()[4])
				
				CPUs_time.append((cpu_total_time, cpu_idle_time))
		
		return CPUs_time
	
	period_start	= get_cpu_time()
	sleep(interval)
	period_stop		= get_cpu_time()
	
	CPUs_percent = []
	for cpu_time_start, cpu_time_stop in zip(period_start, period_stop):
		
		cpu_time = cpu_time_stop[0] - cpu_time_start[0]
		cpu_idle = cpu_time_stop[1] - cpu_time_start[1]
		cpu_percent = ((cpu_time - cpu_idle) / cpu_time) * 100
		
		CPUs_percent.append(cpu_percent)
	
	return CPUs_percent	
		
		
		
		
		
	
while True:
	CPUs_usage = cpu_load(0.5)
	for idx, percent in enumerate(CPUs_usage):
		if idx:
			print "CPU #%s: %.1f" %(idx, percent)
		
		
	
