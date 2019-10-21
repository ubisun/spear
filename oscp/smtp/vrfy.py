#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 3:
	print "Usage : vrfy.py <username> <host>"
	sys.exit(0)

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c=s.connect((sys.argv[2], 25))
banner=s.recv(1024)
print banner
s.send('VRFY ' + sys.argv[1] + '\n')
result = s.recv(1024)
print result
s.close()
