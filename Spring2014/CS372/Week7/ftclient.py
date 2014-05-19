#!/usr/bin/python
# Danny Burrows
# CS372 - Homework 1
# ftserve.py

from socket import *
import sys
import os

# Two connections: 1 for control, 1 for file transfer
# Control - Port 30021, Data - Port 30020

MAXMSG = 1024

class client(object):
	"""
	Client class, which accepts input from the user and interfaces with the server via two connections, the data and control sockets.
	"""
	def __init__(self, host="localhost", controlPort=30021, dataPort=30020, cli=True):
		# control socket info
		self.controlSock = socket(AF_INET, SOCK_STREAM) # create socket
		try:
			self.controlSock.connect((host, controlPort)) # connect to socket
		except:
			self.errorMsg("The server is not available")
		# data socket info
		self.dataSock = socket(AF_INET, SOCK_STREAM)
		self.dataSock.bind(('', dataPort))
		self.dataSock.listen(1)
		# inform server client is ready
		self.controlSock.send("rdy")
		self.data, self.dataAddr = self.dataSock.accept()
		# inform the IP/port connected
		print "Connected to ", self.dataAddr
		# run the main loop
		if not cli:
			self.mainLoop()

	def mainLoop(self):
		"""
		Gets commands from the user, loops until the user quits
		"""
		# a list of commands that the server can handle
		properCommands = ['list', 'quit', 'get', 'cd']
		while True:
			command = raw_input("cmd > ")
			# ensures that command recieved is one that the server can handle
			if command.split()[0] not in properCommands or (command.split()[0] == "get" and len(command.split()) < 2):
				self.printUsage()
			else:
				# command is good, send command to the server
				self.controlSock.send(command)
				# receive response
				response = self.controlSock.recv(MAXMSG)
				if response == "quit":
					self.quit()
				elif response[0:3] == "put":
					self.getFile(response.split()[1], response.split()[2])
				else:
					print response
	
	def processCommand(self, command, file):
		"""
		Handler for processing a command, dictates what action occurs with the client object
		"""
		# a file request
		if command == "get":
			msg = command + " " + file
			self.controlSock.send(msg)
			response = self.controlSock.recv(MAXMSG)
			self.getFile(response.split()[1], response.split()[2])
		# list contents of the directory
		elif command == "list":
			self.controlSock.send(command)
			response = self.controlSock.recv(MAXMSG)
		# displays the servers respnse
		print response
		self.controlSock.send("quit")
		self.quit()

	def getFile(self, fileName, fileSize):
		"""
		Handler for receiving a file, calls the get() method which actually does the lifting
		"""
		# receives the
		self.get(fileName, fileSize)
		# let's server know we are finished writing
		self.controlSock.send("end")

	def quit(self):
		"""
		Shuts down the client and sends a command to the server to shut down.
		"""
		self.controlSock.close()
		self.dataSock.close()
		sys.exit()

	def printUsage(self):
		"""
		Displays how to use the command interface. Displays on error.
		"""
		print "Commands supported:"
		print "list - provides a listing of the files and directories on the server path"
		print "cd - changes the directory on the server"
		print "get <filename> - pulls a text file from the server and stores it in the local directory"
		print "quit - shuts down the server and the client"
		return

	def errorMsg(self, message):
		"""
		General error message.
		"""
		print message
		print "Check your arguments and try again"
		sys.exit()

	def get(self, fileName, fileSize):
		"""
		Receives the file sent from the server.
		"""
		response = ""
		message = ""
		# read the file contents in
		while len(message) < int(fileSize):
			bytesLeft = int(fileSize) - len(message)
			response = self.data.recv(bytesLeft)
			message = message + response
		# writes the file
		print "Writing new file..."
		if os.path.isfile(fileName):
			print "File already exists."
		else:
			output = open(fileName, 'w')
			output.write(message)
			print "File " + fileName + " successfully transferred."

		return

def main(args):
	# simple parsing of te command line arguments.
	try:		
		if len(args) > 1:
			ftclient = client(host=args[1], controlPort=int(args[2]))
			if len(args) == 5:
				file = args[4]
			else:
				file = None
			ftclient.processCommand(args[3], file)
		else:
			ftclient = client(cli=False)
	except:
		# an error occurred
		print "Please check your parameters."
		print "Proper usage is: python ftclient <ip address> <port> <command> <?file>"
		exit()

# main program
if __name__ == "__main__":
	main(sys.argv)