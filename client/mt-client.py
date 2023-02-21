##Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Import socket module
# import socket

import threading
import socket 
import time
import sys
import select


class Client:
	def __init__(self):
		self.host = "127.0.0.1"
		self.port = 2048
		self.s = ''
	def start_client(self):
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	# s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.connect((self.host,self.port))
		while True:
		# message sent to server
		# message received from server
		# ask the client whether he wants to continue
			socket_list = [sys.stdin, self.s]
			# Get the list of sockets which are readable
			rList, wList, error_list = select.select(socket_list , [], [])
			for sock in rList:
				if sock == self.s:
					if self.recevier():
						continue
					else:
						sys.exit()
				else:
					if self.sender():
						continue
					else:
						sys.exit()
		s.close()
	def recevier(self):
		data = self.s.recv(1024)
		# print the received message
		# here it would be a reverse of sent message
		if data:
			print(str(data.decode('ascii')))
			return True
		else:
			return False
	def sender(self):
		ans = input('\n')
		if ans == '':
			ans2 = input('\nDo you want to continue(y/n) :')
			if ans2 =='y':
				return True
			else:
				return False
		else:
			self.s.send(ans.encode('ascii'))
			return True
		
def Main():
    client = Client()
    client.start_client()

if __name__ == '__main__':
	Main()

