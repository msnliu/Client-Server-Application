##Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Import socket module
# import socket

import threading
import socket 
import time
# import sys


def Main():
	host = "127.0.0.1"
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port = 2048
	s.connect((host,port))

	def sender():
		while True:
		# message sent to server
		# message received from server
		# ask the client whether he wants to continue
			ans = input('\n')
			if ans == '':
				ans2 = input('\nDo you want to continue(y/n) :')
				if ans2 =='y':
					continue
				else:
					break
			else:
				s.send(ans.encode('ascii'))	
				continue
		s.close()

	def receiver():
		while True:
			data = s.recv(1024)
			# print the received message
			# here it would be a reverse of sent message
			if data:
				print(str(data.decode('ascii')))

	sender_thread = threading.Thread(target=sender)
	receiver_thread = threading.Thread(target=receiver)

	sender_thread.start()
	receiver_thread.start()

	sender_thread.join()
	receiver_thread.join()

if __name__ == '__main__':
	Main()

