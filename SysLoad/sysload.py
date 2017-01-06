#! /usr/bin/env python



import sys, os, curses

from multiprocessing import cpu_count
from time import sleep


INTERVAL		= 0.5
BAR_CHAR		= "|"
NULL_CHAR		= " "
GRAPH_CHAR		= "*"
AVG_GRAPH_LEN	= 200

	

			
def makeEven(x):
	if x % 2 != 0: x += 1
	return x 	
	
	
	
def cpu_load(interval):
	
	def get_cpu_time(stat_file):
		CPUs_time = []
		stat_file.seek(0)
		stat_out	= stat_file.readlines()
		for line in stat_out:
			if "cpu" in line and line.split()[0]:
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
	
	stat_f			= open("/proc/stat","r")
	
	period_start	= get_cpu_time(stat_f)
	sleep(interval)
	period_stop		= get_cpu_time(stat_f)
	
	stat_f.close()
	
	CPUs_percent	= []
	for cpu_time_start, cpu_time_stop in zip(period_start, period_stop):
		try:
			cpu_time 	= cpu_time_stop[0] - cpu_time_start[0]
			cpu_idle 	= cpu_time_stop[1] - cpu_time_start[1]
			cpu_percent = ((cpu_time - cpu_idle) / cpu_time) * 100
			
		except:
			cpu_percent	= 0
		
		CPUs_percent.append(cpu_percent)
		
	cpu_avg = CPUs_percent[0]
	CPUs_percent.pop(0)	
	
	return CPUs_percent, cpu_avg	
		


def draw_avg_graph(scr, y, x, graph_len, avg):
	
	y += 13
	graph_hight = 10
	scr.addstr(y, x, "-" * graph_len)
	scr.addstr(y - 11, x, "-" * graph_len)


	x_bar = x + graph_len - 1
	for cpu_value in reversed(avg):
		
		avg_bar_hight = int(round(cpu_value / 10))
				
		for y_bar in range(1,11):
			if y_bar <= avg_bar_hight:
				bar_char = GRAPH_CHAR
			else:
				bar_char = NULL_CHAR
				
			scr.addstr(y - y_bar, x_bar, bar_char)	
							
		x_bar -= 1
		if x_bar < x:
			break
			
	return 0



def main(screen):
	
	height_prev	= 0
	width_prev	= 0
	
	cpu_number	= cpu_count()
	fill_cpu	= len(str(cpu_number))
	
	avg_tab = []	
	
	screen.nodelay(True)
	
	while True:
		height, width = screen.getmaxyx()
												
		if height != height_prev or width != width_prev:
			screen.clear()
			screen.border()
			screen.refresh()
			
			scr_x	= (width	* 0.9) - 2
			scr_y	= (height	* 0.9) - 2

			x = makeEven(width	- int(scr_x)) / 2
			y = makeEven(height	- int(scr_y)) / 2
						
		cpus_load, cpus_avg = cpu_load(INTERVAL)
		avg_tab.append(cpus_avg)									
		if len(avg_tab) > AVG_GRAPH_LEN:
			avg_tab.pop(0)		
		
		
		if height > y + len(cpus_load):
				
			for idx, cpu in enumerate(cpus_load):
				
				cpu_header	= "CPU #%s : " % str(idx).zfill(fill_cpu)
				cpu_percent	= "%3.1f %%" % cpu
							
				max_bar_len	=	int(scr_x) - len(cpu_header) - 8
				bar_len		=	int(cpu * max_bar_len) / 100
				
				bar_graph_on 	= BAR_CHAR[0] * bar_len								
				bar_graph_off	=  " " * (max_bar_len - bar_len)
				bar_graph_full	= bar_graph_on + bar_graph_off	
								
				colorized_bar_graph = bar_graph_full
							
				cpu_bar		=  "[" + colorized_bar_graph + "]" 
																			
				screen.addstr(y + idx, x, cpu_header + cpu_bar + cpu_percent.rjust(8))
		else:
			screen.addstr(1,1, "Terminal is too small ;(")		
						
						
		if height > len(cpus_load) + 17:	
			draw_avg_graph(screen, y + len(cpus_load), x + len(cpu_header), len(cpu_bar), avg_tab)
								
		screen.refresh()
			
		height_prev = height
		width_prev	= width	
	
	


if __name__ == "__main__":
	try:
		screen = curses.initscr()
		curses.noecho()
		curses.curs_set(0)
		main(screen)
	except KeyboardInterrupt:
		curses.nocbreak()
		curses.echo()
		curses.endwin()
		


