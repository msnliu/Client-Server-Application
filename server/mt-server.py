#Ref: https://www.geeksforgeeks.org/socket-programming-multi-threading-python/

import socket
import random
from user import User
import re
from _thread import *
import threading

class Server:
    err_msg = 'Please give a valid input as instructed in the documentation'
    def __init__(self):
        self.accountName_table={} # ID to user object
        self.name_list = [] # Username list
        self.connections = {} # from id to connections
        self.connections_id = {}  # from connections to id
        self.host = "127.0.0.1"
        self.port = 2048
        # p_lock = threading.Lock()
    def start_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        print("socket binded to port", self.port)
        # put the socket into listening mode
        s.listen(5)
        print("socket is listening")
    # a forever loop until client wants to exit
        while True:
            # establish connection with client
            c, addr = s.accept()
            print('Connected to :', addr[0], ':', addr[1])
            data = "Please Create or login your account "
            c.send(data.encode('ascii'))
            # Start a new thread and return its identifier
            start_new_thread(self.threaded, (c,))
    def account_creation(self,username,c):
        new_user = User(username)
        self.name_list.append(username)
        accountID = str(new_user.ID)
        self.accountName_table[accountID] = new_user
        # accountMsg_table[accountID] = []
        self.connections[accountID] = c
        self.connections_id[c] = accountID
        print("New User created. key: " + str(accountID) + "\n")
        data = "Success New Account Creation! Your new Account ID: " + str(accountID) + "\n"
        return data

    def list_accounts(self,pattern):
        accountPre = str(pattern)
        rematch = "^" + accountPre + "$"
        print("key: " + str(pattern) + "\n")
        regex = re.compile(rematch)
        matches = [string for string in [val.name for _, val in self.accountName_table.items()] if re.match(regex, string)]

        if len(matches):
            
            for m in range(len(matches)):
                print("Account matched: " + matches[m] + "\n")

            data = "Account matched: " + ','.join(matches) +"\n"
        # matching account doesn't exist, no account ID is associated
        else:
            print("Account matched doesnt exist: " + str(accountPre)  + "\n")
            data = "Account matched to: " +  str(accountPre) + " doesn't exist \n"
        return data
    def send_message(self,name,msg,c):
        receiver = name
        if receiver in self.name_list:
            for id, user in self.accountName_table.items():
                if user.name == receiver:
                    rscv_ID = str(user.ID)
            sender = self.accountName_table[self.connections_id[c]].name
            message = str(sender) + " sends: "+  str(msg) + "\n"
            if self.accountName_table[rscv_ID].active:
                client = self.connections[rscv_ID]
                data = "message delivered\n"
                client.send(message.encode('ascii'))
                print("Sender " +  str(sender) + " sends a new message " + str(msg) + " to " + str(receiver) + "\n")
            else:
                data = "message delivered to mailbox\n"
                self.accountName_table[rscv_ID].queue.append(message)
                print("message from " + sender + " has been delivered to " + receiver + "'s mailbox\n")
        else:
            print("Receiver doesnt exist: " + str(receiver)  + "\n")
            data = "Receiver: " +  str(receiver) + " doesn't exist \n"
        return data
    def pop_undelivered(self,id):
        accountID = str(id)
        user = self.accountName_table[accountID]
        q = user.queue
        if q:
            data = f"undelivered message for user ID {accountID}: \n" 
            while q:
                new_msg = q.pop(0)
                data += new_msg + "\n"
        else:
            data = "No new messages\n"
        return data
    def delete_account(self,id):
        accountID = str(id)
        try:
            user = self.accountName_table[accountID]
        except:
            return "User Not Found! "
        name = user.name
        q = user.queue
        if q:
            data = "Please check your mailbox before deleting your account! \n"
            return data
        else:
            self.name_list.remove(name)
            old_c = self.connections[accountID]
            del self.connections_id[old_c]
            del self.connections[accountID]
            del self.accountName_table[accountID]
        print("Account ID: " +  str(accountID) + " has been deleted" + "\n")
        data = "Your account has been deleted\n"
        return data
    # thread function
    def threaded(self,c):
        while True:
            data_list=[]
            # data received from client
            data = c.recv(1024)
            data_str = data.decode('UTF-8')
            # Log out
            if not data:
                if c in self.connections_id.keys():
                    userid = self.connections_id[c]
                    user = self.accountName_table[userid]
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
                    if(str(data_list[1]) in self.accountName_table.keys()):
                        user = self.accountName_table[str(data_list[1])]
                        user.active = True
                        self.connections[str(data_list[1])] = c
                        self.connections_id[c] = str(data_list[1])
                        print(f'user : {user.name} is now logged in\n')
                        data = f'user : {user.name} is now logged in\n'
                    else:
                        data = f'user with ID : {data_list[1]} is not recognized in the system, please try a different name or create a new one\n'
                    c.send(data.encode('ascii'))
                except:
                    c.send(self.err_msg.encode('ascii'))
            elif opcode == '1':
                #account creation
                try:
                    username = str(data_list[1])
                    data = self.account_creation(username,c)
                    c.send(data.encode('ascii'))
                except:
                    c.send(self.err_msg.encode('ascii'))
            elif opcode == '2':
                try:
                    if(len(data_list) == 1):
                        data = "Showing all accounts: " + ','.join(self.name_list) +"\n"
                        print("Output all accounts name: " + "\n")
                    else:
                        data = self.list_accounts(data_list[1])
                except:
                    c.send(self.err_msg.encode('ascii'))
                #list accounts
                c.send(data.encode('ascii')) 
            elif opcode == '3':
                #Send a message to a recipient
                try:
                    username = str(data_list[1])
                    msg = str(data_list[2])
                    data = self.send_message(username,msg,c)
                    c.send(data.encode('ascii'))
                except:
                    c.send(self.err_msg.encode('ascii'))
                #list accounts
            elif opcode == '4':
                try:
                    userid = str(data_list[1])
                    data = self.pop_undelivered(userid)
                    c.send(data.encode('ascii'))
                except:
                    c.send(self.err_msg.encode('ascii'))
            elif opcode == '5':
                #Delete an account
                try:
                    userid = str(data_list[1])
                    data = self.delete_account(userid)
                    c.send(data.encode('ascii'))
                except:
                    c.send(self.err_msg.encode('ascii'))
            else:
                c.send(self.err_msg.encode('ascii'))
        # connection closed
        # When no user was attached to the current connection
        try:
            del self.connections_id[c]
        except:
            pass
        c.close()
def Main():
    server = Server()
    server.start_server()
    # s.close()
if __name__ == '__main__':
    Main()
