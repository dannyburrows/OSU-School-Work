# Danny Burrows
# ftserve.py

import socket

HOST = ''
CONTROLPORT = 30021
DATAPORT = 30020

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, CONTROLPORT))
s.listen(1)
while 1:
	connection, address = s.accept()
	print "Connected to", address
	data = connection.recv(1024)
	if not data: break
	connection.sendall(data)

connection.close()