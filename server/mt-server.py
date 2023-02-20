#Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

import socket
# import mysql.connector
import random
from user import User
import re

# import thread module
from _thread import *
import threading

accountName_table={}
# accountMsg_table={}
name_list = []
connections = {} # id to connections
connections_id = {}

p_lock = threading.Lock()

# thread function
def threaded(c):
    while True:
        data_list=[]
        # data received from client
        data = c.recv(1024)
        data_str = data.decode('UTF-8')
        
        if not data:
            userid = connections_id[c]
            username = accountName_table[userid].name
            print(username + " has logged out of the system\n")
            break
        # print user input
        print(data_str+"\n")
        
        # parse user input
        data_list = data_str.split('|')
        opcode = data_list[0]
        
        print("Opcode:" + str(opcode))

        if opcode == '0':
            if(str(data_list[1]) in accountName_table.keys()):
                user = accountName_table[str(data_list[1])]
                user.active = True
                old_c = connections[str(data_list[1])]
                del connections_id[old_c]
                connections[str(data_list[1])] = c
                connections_id[c] = str(data_list[1])
                print(f'user : {user.name} is now logged in\n')
            else:
                print(f'user with ID : {data_list[1]} is not recognized in the system, please try a different name or create a new one\n')
        elif opcode == '1':
            #account creation
            new_user = User(str(data_list[1]))
            name_list.append(str(data_list[1]))
            accountID = str(new_user.ID)
            accountName_table[accountID] = new_user
            # accountMsg_table[accountID] = []
            connections[accountID] = c
            connections_id[c] = accountID
            print("New User created. key: " + str(accountID) + "\n")
            data = "Account ID: " + str(accountID) + "\n"
            c.send(data.encode('ascii')) 
            
        elif opcode == '2':
            #list accounts
            accountPre = str(data_list[1])
            rematch = "^" + accountPre + "$"
            print("key: " + str(data_list[1]) + "\n")
            
            regex = re.compile(rematch)
            matches = [string for string in [val.name for _, val in accountName_table.items()] if re.match(regex, string)]

            if len(matches):
                
                for m in range(len(matches)):
                    print("Account matched: " + matches[m] + "\n")

                data = "Account matched: " + ','.join(matches) +"\n"

            # matching account doesn't exist, no account ID is associated
            else:
                print("Account matched doesnt exist: " + str(accountPre)  + "\n")
                data = "Account matched to: " +  str(accountPre) + " doesn't exist \n"
            c.send(data.encode('ascii')) 

        elif opcode == '4':
            accountID = connections_id[c]
            user = accountName_table[accountID]
            q = user.queue
            
            if q:
                data = ""
                while q:
                    new_msg = q.pop(0)
                    data += new_msg + "\n"
            else:
                data = "No new messages\n"
            c.send(data.encode('ascii'))

        elif opcode == '3':
            #Send a message to a recipient

            receiver = data_list[1]
            
            if receiver in name_list:
                
                for id, user in accountName_table.items():
                    if user.name == receiver:
                        rscv_ID = str(user.ID)

                sender = accountName_table[connections_id[c]].name

                client = connections[rscv_ID]
                msg = data_list[2]
                
                message = str(sender) + " sends: "+  str(msg) + "\n"
                if accountName_table[rscv_ID].active:
                    c.send("message delivered\n".encode('ascii'))
                    client.send(message.encode('ascii'))
                    print("Sender " +  str(sender) + " sends a new message " + str(msg) + " to " + str(receiver) + "\n")
                else:
                    c.send("message delivered to mailbox\n".encode('ascii'))
                    accountName_table[rscv_ID].queue.append(message)
                    print("message from " + sender + " has been delivered to " + receiver + "'s mailbox\n")

            else:
                print("Receiver doesnt exist: " + str(receiver)  + "\n")
                data = "Receiver: " +  str(receiver) + " doesn't exist \n"
                c.send(data.encode('ascii'))

        elif opcode == '5':
            #Delete an account
            accountID = data_list[1]
            user = accountName_table[accountID]
            name = user.name
            q = user.queue
            l = len(data_list)
            if q and l == 2:
                data = "Please check your mailbox before deleting your account! If you would like to delete immediately, please try again by adding |f after optcode 5\n"
                c.send(data.encode('ascii')) 
                continue
            else:
                name_list.remove(name)
                del connections[accountID]
                del connections_id[c]
                del accountName_table[accountID]
            
            print("Account ID: " +  str(accountID) + " has been deleted" + "\n")
            data = "Your account has been deleted\n"
            c.send(data.encode('ascii')) 

        else:
            data = "Invalid Request\n"
            c.send(data.encode('ascii'))
    
    # connection closed
    user = accountName_table[connections_id[c]]
    user.active = False
    c.close()

def Main():

    host = "127.0.0.1"
 
    # reserve a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 2048
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
        
    # s.close()
 
 
if __name__ == '__main__':
    Main()
