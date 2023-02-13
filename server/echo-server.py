#Ref: https://realpython.com/python-sockets/

import socket

HOST = '10.0.0.160'
PORT = 2048
#update firewall for TCP traffic on port 2048

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            #print the data
            print((str(data)+"\n"))
            conn.sendall(data)