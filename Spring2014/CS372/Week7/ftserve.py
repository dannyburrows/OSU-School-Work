#!/usr/bin/python
# Danny Burrows
# CS372 - Homework 1
# ftserve.py

from socket import *
import os
import sys

MAXMSG = 1024

class controlSock:
	"""
	Class for the controlling socket
	"""
	def __init__(self, controlPort=30021, dataPort=30020):
		"""
		Initalize the class
		"""
		self.dataPort = dataPort
		self.connect = None
		self.controlSock = socket(AF_INET, SOCK_STREAM)
		self.controlPort = controlPort
		print "Server is listening"
		self.controlSock.bind(("", self.controlPort))
		self.controlSock.listen(1)
		self.mainLoop()

	def mainLoop(self):
		"""
		Main handler for the controlSock class. Loops until a quit message is recieved from the client.
		Sends commands and parses responses from the server.
		"""
		while True:
			# connection is the object that will control sending/receiving
			# address is a tuple of the socket, IP first, port second
			self.connection, address = self.controlSock.accept()
			print "Server Status: Ready"
			print "Connected to: ", address
			request = self.connection.recv(MAXMSG)
			# client is ready
			if request == "rdy":
				self.dataSock = dataSock(address[0],self.dataPort)
			while True:
				# error message will print on the client if an error is found anywhere
				errorMsg = None
				# msg will print on the client if everything goes smoothly
				msg = ""

				# received the command and call functions
				command = self.connection.recv(MAXMSG)
				print "Command > ", command
				# list the current directory on the server
				if command == "list":
					msg = self.listDir()
				# change the directory on the server
				elif command[0:2] == "cd":
					# get just the directory name
					newDir = command[3:]
					# try to change the directory, throws an error if directory does not exist
					try:
						os.chdir(newDir)
						msg = self.listDir()
					# catch error
					except:
						errorMsg = "Directory does not exist"
				# shut down the server and the client
				elif command == "quit":
					self.shutDown()
				elif command[0:3] == "get":
					fileName = command.split()[1]
					if os.path.isfile(fileName):
						fileSize = os.path.getsize(fileName)
						ready = "put " + fileName + " " + str(fileSize)
						self.connection.send(ready)
						self.dataSock.put(fileName, fileSize)
						if self.connection.recv(MAXMSG) == "end":
							print "File uploaded"
					else:
						errorMsg = "File does not exist"

				# return the proper message to the client
				if errorMsg:
					self.connection.send(errorMsg)
				else:
					self.connection.send(msg)

	def listDir(self):
		"""
		Lists the current directory on the server.
		"""
		directory = os.listdir(os.curdir)
		ls = "" # empty string for directory
		for file in directory:
			ls = ls + file + "\n"
		return ls

	def shutDown(self):
		"""
		Closes the control socket and quits the program.
		"""
		# send a message to shut the client down too
		self.connection.send("quit")
		# shut the server down
		self.controlSock.close()
		sys.exit()

class dataSock:
	"""
	The socket for the datastream on the server. 
	"""
	def __init__(self, host, dataPort):
		self.dataSock = socket(AF_INET, SOCK_STREAM)
		self.dataSock.connect((host, dataPort))

	def put(self, fileName, fileSize):
		"""
		Reads a file byte by byte, sends the data over the socket connection
		"""
		# read file in
		input = open(fileName, 'r').read()
		sent = 0 # number of bytes sent
		while sent < fileSize:
			read = self.dataSock.send(input[sent:])
			sent = sent + read

if __name__ == "__main__":
	controlSock()