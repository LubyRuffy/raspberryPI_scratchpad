#! /usr/bin/env python


from bspots 	import BSpots
from random		import randint
import time, cv2, sys, curses

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4


if __name__ == "__main__":
	
	try:
	        screen = curses.initscr()
		curses.noecho()
		curses.curs_set(0)
		screen.nodelay(True)

		screen.clear()
		screen.border()
		screen.refresh()
			
		expected_fps	= 15
		frames		= 0
                fps             = 0
		period		= 1		
		prev_time	= time.time()
		delay		= 1.0 / expected_fps
			
		cam = cv2.VideoCapture(0)
		cam_x = 320
		cam_y = 240
		cam.set(3, cam_x)
		cam.set(4, cam_y)

		bs = BSpots()	
		while True:
			
			curr_time = time.time()			

			ret, cam_grab = cam.read()		
					
			if ret:
				bs.get_image_from_CAM(cam_grab)											
				crds	= bs.analize_image()
				coords	= crds[0] if len(crds) > 0 else []  	
				bs.flush()
				screen.refresh()
				scr_y, scr_x = screen.getmaxyx()
				
				X = int(((scr_x - 2) * coords['X']) / float(cam_x)) + 1
				Y = int(((scr_y - 2) * coords['Y']) / float(cam_y)) + 1
				
				screen.clear()
				screen.border()
				screen.addstr(Y, X, "*")
				screen.addstr(1, 2, "FPS: {0}".format(round(fps, 2)))
				screen.addstr(2, 2, "Screen res   : X: {0:<3} Y: {1:<3}".format(scr_x, scr_y))
				screen.addstr(3, 2, "Point coords : X: {0:<3} Y: {1:<3}".format(X, Y))
				
				screen.refresh()			
							
				time.sleep(delay)
				frames += 1
				if curr_time - prev_time >= period:				
					fps         = frames / (curr_time - prev_time) 
					frames	    = 0
					prev_time   = curr_time
					delay       = (fps * delay) / float(expected_fps)

        except:
			curses.nocbreak()
			curses.echo()
			curses.endwin()
			
