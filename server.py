# Echo server program
import socket
import sys
import json
from thread import *
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
			sendList = [self.__hit, self.__queue[self.__count:self.__count+1000]]
			self.__count += 1000
			if self.__count % 50000 == 0:
				print self.__count
			self.__hit += 1
			conn.sendall(json.dumps(sendList))
			# print 'Sent ', sendList
		else:
			conn.sendall(json.dumps([]))
			# print 'Sent []'
		conn.close()

	def start(self):
		client_list = [['', 50001], ['', 50002], ['', 50003]]

		print 'Please enter command: '
		command = raw_input()

		for client in client_list:
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.connect((client[0], client[1]))
				if command == "process":
					s.sendall(command)
					self.__process()
				else:
					s.sendall(command)
			except:
				print 'Error while connecting'
				print sys.exc_info()

	def __process(self):
		self.__queue = range(1, 10000)
		self.__count = 0
		self.__hit = 0

		self.__updatedQueue = []

		while self.__count < len(self.__queue):
			conn, addr = self.__socket.accept()
			# print 'Connected by', addr
			if not self.__start:
				self.__time = time.time()
				self.__start = True
			start_new_thread(self.__clientthread, (conn,))

		self.sort()


	def sort(self):
		time.sleep(2)
		self.__updatedQueue.sort(key=lambda x: x[0])
		print self.__updatedQueue
		print time.time() - self.__time - 2

	def stop(self):
		self.__socket.close()

def main():
	server = Server()
	server.start()
	server.stop()

if __name__ == "__main__":
	main()
