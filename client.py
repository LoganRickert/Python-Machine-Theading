# Echo client program
import socket
import time
import pickle
import random


class Client(object):

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

	def processData(data):
		for i in range(0, len(data[1])):
			data[1][i] += 5
		return data

what = [-1]

while what != []:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))
		if len(what) == 2:
			what = processData(what)
			time.sleep(1)
			print 'Sending ', what
			s.sendall(pickle.dumps(what))
		else:
			s.sendall(pickle.dumps([]))
		data = s.recv(1024)
		s.close()
		what = pickle.loads(data)
		print 'Received ', what
	except:
		print 'Error while connecting'
		what = []

def main():
	client = Client()
	client.start()

if __name__ == "__main__":
	main()