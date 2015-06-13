# Echo server program
import socket
import sys
import json
from thread import *
from threading import Thread
import time

class Server(object):

	def __init__(self):
		self.__host = ''
		self.__port = 50000
		# self.__set_port()

		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.__socket.bind((self.__host, self.__port))
		self.__socket.listen(5)

		self.__queue = []
		self.__count = 0
		self.__hit = 0

		self.__time = 0
		self.__start = False

		self.__threads = []

		self.__process_start = False

		self.__hasFinishedProcessing = False

	def __set_port(self):
		with open('port', 'r') as f:
			self.__port = int(f.read())
		self.__port += 1
		with open('port', 'w') as f:
			f.write(str(self.__port))

	def __clientthread(self, conn):
		data = conn.recv(2048)
		temp_data = data

		while temp_data != "" and len(temp_data) > 2047:
			temp_data = conn.recv(2048)
			data += temp_data

		if data:
			addQueue = json.loads(data)
			if len(addQueue) > 0:
				# print 'recv the data ', addQueue
				self.__updatedQueue.append(addQueue)
		if self.__count < len(self.__queue):
			sendList = [self.__hit, self.__queue[self.__count:self.__count+10]]
			self.__count += 10
			if self.__count % 25000 == 0:
				print self.__count
			self.__hit += 1
			conn.sendall(json.dumps(sendList))
			# print 'Sent ', sendList
		else:
			self.__hasFinishedProcessing = True
			conn.sendall(json.dumps([]))
			# print 'Sent []'
		conn.close()

	def start(self):
		client_list = [['', 50001], ['', 50002], ['', 50003]]

		print 'Please enter command: '
		command = raw_input()

		threads = []

		for client in client_list:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((client[0], client[1]))
				if command == "process":
					s.sendall(command)
					t = Thread(target=self.__process)
					t.start()
					threads.append(t)
				else:
					s.sendall(command)
			except:
				print 'Error while connecting'
				print sys.exc_info()

		for t in threads:
			t.join()

	def __process(self):
		if not self.__process_start:
			self.__process_start = True
			self.__queue = range(1, 501)
			self.__count = 0
			self.__hit = 0

			self.__updatedQueue = []

			self.__threads = []

			while not self.__hasFinishedProcessing:
				conn, addr = self.__socket.accept()
				# print 'Connected by', addr

				if not self.__start:
					self.__time = time.time()
					self.__start = True

				t = Thread(target=self.__clientthread, args=(conn,))
				t.start()
				self.__threads.append(t)

			# Need one final accept
			conn, addr = self.__socket.accept()
			t = Thread(target=self.__clientthread, args=(conn,))
			t.start()
			self.__threads.append(t)

			for t in self.__threads:
				t.join()

			self.sort()
		else:
			print 'process is already started'

	def sort(self):
		print 'Threads have joined'
		self.__updatedQueue.sort(key=lambda x: x[0])
		print self.__updatedQueue
		print time.time() - self.__time

	def stop(self):
		self.__socket.close()

def main():
	server = Server()
	server.start()
	server.stop()

if __name__ == "__main__":
	main()
