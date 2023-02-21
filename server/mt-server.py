#Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

import socket
import random
from user import User
import re
from _thread import *
import threading

accountName_table={} # ID to user object
name_list = [] # Username list
connections = {} # from id to connections
connections_id = {}  # from connections to id
# p_lock = threading.Lock()
err_msg = 'Please give a valid input as instructed in the documentation'

def account_creation(username,c):
    new_user = User(username)
    name_list.append(username)
    accountID = str(new_user.ID)
    accountName_table[accountID] = new_user
    # accountMsg_table[accountID] = []
    connections[accountID] = c
    connections_id[c] = accountID
    print("New User created. key: " + str(accountID) + "\n")
    data = "Success New Account Creation! Your new Account ID: " + str(accountID) + "\n"
    return data

def list_accounts(pattern):
    accountPre = str(pattern)
    rematch = "^" + accountPre + "$"
    print("key: " + str(pattern) + "\n")
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
    return data
def send_message(name,msg,c):
    receiver = name
    if receiver in name_list:
        for id, user in accountName_table.items():
            if user.name == receiver:
                rscv_ID = str(user.ID)
        sender = accountName_table[connections_id[c]].name
        message = str(sender) + " sends: "+  str(msg) + "\n"
        if accountName_table[rscv_ID].active:
            client = connections[rscv_ID]
            data = "message delivered\n"
            client.send(message.encode('ascii'))
            print("Sender " +  str(sender) + " sends a new message " + str(msg) + " to " + str(receiver) + "\n")
        else:
            data = "message delivered to mailbox\n"
            accountName_table[rscv_ID].queue.append(message)
            print("message from " + sender + " has been delivered to " + receiver + "'s mailbox\n")
    else:
        print("Receiver doesnt exist: " + str(receiver)  + "\n")
        data = "Receiver: " +  str(receiver) + " doesn't exist \n"
    return data
def pop_undelivered(id):
    accountID = str(id)
    user = accountName_table[accountID]
    q = user.queue
    if q:
        data = f"undelivered message for user ID {accountID}: \n" 
        while q:
            new_msg = q.pop(0)
            data += new_msg + "\n"
    else:
        data = "No new messages\n"
    return data
def delete_account(id):
    accountID = str(id)
    user = accountName_table[accountID]
    name = user.name
    q = user.queue
    if q:
        data = "Please check your mailbox before deleting your account! \n"
        return data
    else:
        name_list.remove(name)
        del connections[accountID]
        del accountName_table[accountID]
    print("Account ID: " +  str(accountID) + " has been deleted" + "\n")
    data = "Your account has been deleted\n"
    return data
# thread function
def threaded(c):
    while True:
        data_list=[]
        # data received from client
        data = c.recv(1024)
        data_str = data.decode('UTF-8')
        # Log out
        if not data:
            if c in connections_id.keys():
                userid = connections_id[c]
                user = accountName_table[userid]
                username = user.name
                user.active = False
                print(username + " has logged out of the system\n")
            break
        # print user input
        print(data_str+"\n")
        # parse user input
        data_list = data_str.split('|')
        opcode = data_list[0]
        print("Opcode:" + str(opcode))
        # Login
        if opcode == '0':
            try:
                if(str(data_list[1]) in accountName_table.keys()):
                    user = accountName_table[str(data_list[1])]
                    user.active = True
                    connections[str(data_list[1])] = c
                    connections_id[c] = str(data_list[1])
                    print(f'user : {user.name} is now logged in\n')
                    data = f'user : {user.name} is now logged in\n'
                else:
                    data = f'user with ID : {data_list[1]} is not recognized in the system, please try a different name or create a new one\n'
                c.send(data.encode('ascii'))
            except:
                c.send(err_msg.encode('ascii'))
        elif opcode == '1':
            #account creation
            try:
                username = str(data_list[1])
                data = account_creation(username,c)
                c.send(data.encode('ascii'))
            except:
                c.send(err_msg.encode('ascii'))
        elif opcode == '2':
            try:
                if(len(data_list) == 1):
                    data = "Showing all accounts: " + ','.join(name_list) +"\n"
                    print("Output all accounts name: " + "\n")
                else:
                    data = list_accounts(data_list[1])
            except:
                c.send(err_msg.encode('ascii'))
            #list accounts
            c.send(data.encode('ascii')) 
        elif opcode == '3':
            #Send a message to a recipient
            try:
                username = str(data_list[1])
                msg = str(data_list[2])
                data = send_message(username,msg,c)
                c.send(data.encode('ascii'))
            except:
                c.send(err_msg.encode('ascii'))
            #list accounts
        elif opcode == '4':
            try:
                userid = str(data_list[1])
                data = pop_undelivered(userid)
                c.send(data.encode('ascii'))
            except:
                c.send(err_msg.encode('ascii'))
        elif opcode == '5':
            #Delete an account
            try:
                userid = str(data_list[1])
                data = delete_account(userid)
                c.send(data.encode('ascii'))
            except:
                c.send(err_msg.encode('ascii'))
        else:
            c.send(err_msg.encode('ascii'))
    # connection closed
    del connections_id[c]
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
        if(c in connections_id.keys()):
            data = accountName_table[connections_id[c]].name + ' > '
        else:
            data = "Please Create or login your account "
        c.send(data.encode('ascii'))
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    # s.close()
if __name__ == '__main__':
    Main()
