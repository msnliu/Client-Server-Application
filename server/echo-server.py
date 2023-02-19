#Ref: https://realpython.com/python-sockets/

import socket

HOST = '127.0.0.1'
PORT = 2048
#update firewall for TCP traffic on port 2048

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
