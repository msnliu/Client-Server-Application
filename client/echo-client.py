#Ref: https://realpython.com/python-sockets/
import socket

HOST = "10.0.0.160"  # The server's hostname or IP address
PORT = 2048  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall("Hello, world")
    data = s.recv(1024)

print(f"Received {data!r}")