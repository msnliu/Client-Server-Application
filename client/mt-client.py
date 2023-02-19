##Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Import socket module
import socket


def Main():
	# local host IP '127.0.0.1'
	host = "127.0.0.1"

	# Define the port on which you want to connect
	port = 2048

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	# connect to server on local computer
	s.connect((host,port))

	# message you send to server
	#message = "V for vendetta"
	while True:
		# message sent to server
		# message received from server
		# ask the client whether he wants to continue
		ans = input('\nEnter your request:')
		if ans == '':
			ans2 = input('\nDo you want to continue(y/n) :')
			if ans2 =='y':
				continue
			else:
				break
		else:
			s.send(ans.encode('ascii'))
			data = s.recv(1024)
			# print the received message
			# here it would be a reverse of sent message
			print('Received from the server :',str(data.decode('ascii')))
			continue
	# close the connection
	s.close()

if __name__ == '__main__':
	Main()
