#! /usr/bin/env python

import socket, time
 
TCP_IP		= ''
TCP_PORT	= 7018
BUFFER		= 128
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))

try:
	s.listen(0)
	while True:
		pkg_count = 0
		print "\nWaiting for connection ..."
		conn, addr = s.accept()
		print 'Connection address:', addr
		print "\nWaiting for data ..."
		while pkg_count < 2:
			data = conn.recv(BUFFER)
			pkg_count += 1
			timestamp = time.ctime()
			print "{0} - {1}".format(timestamp, data)
		
		#conn.send("AR03")
		
except KeyboardInterrupt:
	conn.close()
	
	
