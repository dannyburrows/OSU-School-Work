import socket

HOST = 'localhost'
PORT = 30021

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.sendall("This is a test")
data = s.recv(1024)
s.close()
print "Received\n", repr(data)