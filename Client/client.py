##Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
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
		"""
		This function continuously reads input from the user and sends it to the server.
		If the user inputs "bye" or "quit", the function will break the loop and shutdown 
		the write end of the socket, and then exit the system. The function adds a short 
		delay after sending the data. 
		"""
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
		"""
		This function continuously listens for incoming messages from the server. 
		If there is incoming data, it will print the received message. If there is an error,
		the loop will break and the function will exit the system. 
		"""
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

