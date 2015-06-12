# Echo server program
import socket
import pickle
from thread import *

class Server(object):

	def __init__(self):
		self.__host = ''
		self.__port = 50000
		self.__set_port()

		self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.__socket.bind((self.__host, self.__port))
		self.__socket.listen(5)

		self.__queue = []
		self.__count = 0
		self.__hit = 0

	def __set_port(self):
		with open('port', 'r') as f:
			self.__port = int(f.read())
		self.__port += 1
		with open('port', 'w') as f:
			f.write(str(self.__port))

	def __clientthread(self, conn):
		data = conn.recv(1024)
		if data:
			addQueue = pickle.loads(data)
			if len(addQueue) > 0:
				print 'recv the data ', addQueue
				self.__updatedQueue.append(addQueue)
		if self.__count < len(self.__queue):
			sendList = [self.__hit, self.__queue[self.__count:self.__count+2]]
			self.__count += 2
			self.__hit += 1
			conn.sendall(pickle.dumps(sendList))
			print 'Sent ', sendList
		else:
			conn.sendall(pickle.dumps([]))
			print 'Sent []'
		conn.close()

	def start(self):
		self.__queue = range(1, 101)
		self.__count = 0
		self.__hit = 0

		self.__updatedQueue = []

		while self.__count < len(self.__queue):
			conn, addr = self.__socket.accept()
			print 'Connected by', addr
			start_new_thread(self.__clientthread, (conn,))

		self.__updatedQueue.sort(key=lambda x: x[0])
		print self.__updatedQueue

def main():
	server = Server()
	server.start()

if __name__ == "__main__":
	main()
