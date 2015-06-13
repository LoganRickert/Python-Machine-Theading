# Echo client program
import socket
import time
import json
import random
import sys
import os

class Client(object):

	def __init__(self, port):
		self.__host = ''
		self.__port = port

		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__socket.bind((self.__host, self.__port))
		self.__socket.listen(5)

		self.__commands = {
			'stop': self.__stop,
			'process': self.__process,
			'print': self.__print,
			'restart': self.__restart,
			'bash': self.__bash
		}

		self.__keepRunning = True

	def start(self):
		while self.__keepRunning:
			conn, addr = self.__socket.accept()
			data = conn.recv(2048)
			temp_data = data

			while temp_data != "" and len(temp_data) > 2047:
				temp_data = conn.recv(2048)
				data += temp_data

			arguments = data.split()

			print 'Recieved command: ' +  arguments[0], arguments[1:]

			try:
				if arguments[0] in self.__commands:
					self.__commands[arguments[0]](arguments[1:])
			except ex:
				print ex 

	def __stop(self, arguments = []):
		self.__keepRunning = False

	def __restart(self, arguments = []):
		print 'restarting...'
		self.__stop()
		self.stop()
		print 'starting...'
		os.execv(sys.executable, [sys.executable] + sys.argv)

	def __print(self, arguments = []):
		print 'hello!'

	def __bash(self, arguments = []):
		op = os.popen(" ".join(arguments))
		print op.read()

	def stop(self):
		print 'closing server...'
		self.__socket.close()

	def __processData(self, data):
		for i in range(0, len(data[1])):
			data[1][i] += 5
		return data

	def __process(self, arguments = []):
		what = [-1]

		host = ''
		port = 50000

		while what != []:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				s.connect((host, port))
				if len(what) == 2:
					what = self.__processData(what)
					s.sendall(json.dumps(what))
				else:
					s.sendall("{}")

				temp_data = s.recv(1024)
				data = temp_data

				while temp_data:
					temp_data = s.recv(1024)
					data += temp_data

				s.close()
				what = json.loads(data)
				# print 'Received ', what
			except:
				print 'Error while connecting'
				print sys.exc_info()
				what = []

		print 'done.'

def main():
	port = 50001

	if len(sys.argv) > 1:
		port = int(sys.argv[1])

	client = Client(port)
	client.start()
	client.stop()

if __name__ == "__main__":
	main()
