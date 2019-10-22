#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 2:
	print "Usage : vrfy.py <host>"
	sys.exit(0)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c=s.connect((sys.argv[1], 25))
banner=s.recv(1024)
print banner

f = open("users.txt", "r")
while True:
	user = f.readline()
	if not user:
		break
	s.send('VRFY ' + user)
	result = s.recv(1024)
	print result

s.close()
f.close()
