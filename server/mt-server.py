#Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

import socket
import mysql.connector
import random

import re

# import thread module
from _thread import *
import threading

accountName_table={}
accountMsg_table={}

p_lock = threading.Lock()

# thread function
def threaded(c):
    while True:
        data_list=[]
        # data received from client
        data = c.recv(1024)
        data_str = data.decode('UTF-8')
        
        if not data:
            print('Bye')
            break
        # print user input
        print(data_str+"\n")
        
        # parse user input
        data_list = data_str.split('|')
        opcode = data_list[0]
        
        print("Opcode:" + str(opcode))

        if opcode == '1':
            #account creation

            accountID  = str(random.randint(0,1000))
            accountName_table[accountID] = str(data_list[1])
            accountMsg_table[accountID] = []
            print("key: " + str(accountID) + "\n")
            data = "Account ID: " + str(accountID) + "\n"
            
        elif opcode == '2':
            #list accounts
            # will not show account id and messages

            accountPre = str(data_list[1])
            print("key: " + str(data_list[1]) + "\n")
            
            regex = re.compile(accountPre)
            matches = [string for string in [val for _, val in accountName_table.items()] if re.match(regex, string)]

            if len(matches):
                
                for m in range(len(matches)):
                    print("Account matched: " + matches[m] + "\n")

                data = "Account matched: " + ','.join(matches) +"\n"

            # matching account doesn't exist, no account ID is associated
            else:
                print("Account matched doesnt exist: " + str(accountPre)  + "\n")
                data = "Account matched to: " +  str(accountPre) + " doesn't exist \n"

        elif opcode == '3':
            #Send a message to a recipient

            sender = accountName_table[data_list[1]]
            print("Sender: " + str(sender) + "\n")

            receiver = data_list[2]
            
            if receiver in accountName_table.values():
                
                print("receiver found: " + str(receiver) + "\n")
                
                for id, name in accountName_table.items():
                    if name == receiver:
                        rscv_ID = id

                msg = data_list[3]
                # If the recipient is logged in, deliver immediately; otherwise queue the message and deliver on demand?
                if # online:
                    accountMsg_table[rscv_ID].append(msg)
                    print("Sender: " +  str(sender) + " sends a new message to: "+  str(receiver) + "\n")
                    data = "Sender: " +  str(sender) + " sends: "+  str(msg) + "\n"
                else:
                    # queue the message

            else:
                print("Receiver doesnt exist: " + str(receiver)  + "\n")
                data = "Receiver: " +  str(receiver) + " doesn't exist \n"

        elif opcode == '4':
            #Delete an account

            accountID = data_list[1]
            del accountMsg_table[accountID]
            del accountMsg_table[accountID]
            data = "Account ID: " +  str(accountID) + " has been deleted" + "\n"

        else:
            data = "Invalid Request\n"

        # send back reversed string to client
        c.send(data.encode('ascii')) 
    
    # connection closed
    c.close()

def Main():

    host = "127.0.0.1"
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 2048
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        c, addr = s.accept()      
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()
 
 
if __name__ == '__main__':
    Main()
