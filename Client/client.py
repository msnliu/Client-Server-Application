##Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Import socket module
# import socket

import threading
import socket 
import time
import sys


def Main():
	host = "127.0.0.1"
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	# s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	port = 2023
	s.connect((host,port))
		
	def sender():
		while True:
		# message sent to server
		# message received from server
		# ask the client whether he wants to continue
			ans = input('\n')
			if ans == ('bye' or 'quit'):
				# s.send(''.encode('ascii'))	
				break
			else:
				s.send(ans.encode('ascii'))	
				time.sleep(0.1)  # add a short delay after sending the data
				continue
		s.shutdown(socket.SHUT_WR)  # close the write end of the socket
		sys.exit()

	def receiver():
		while True:
			try:
				data = s.recv(1024)
				# print the received message
				# here it would be a reverse of sent message
				if data:
					print(str(data.decode('ascii')))
				else:
					sys.exit()
			except:
				break
		# s.close()
		sys.exit()

	sender_thread = threading.Thread(target=sender)
	receiver_thread = threading.Thread(target=receiver)

	sender_thread.start()
	receiver_thread.start()

	sender_thread.join()
	receiver_thread.join()
	s.close()

if __name__ == '__main__':
	Main()

