# cs262-HW1 Guangya Wan & Zongjun Liu

## About
This code implements a chat server using socket programming in Python with multi-threading. It allows the creation of new user accounts, searching for existing accounts, sending messages to other users, and deleting user accounts. The chat server is capable of handling multiple clients at the same time. Two methods(custom wire proctol and gRPC) were implemented 

## First Implementation (Custom Wire Protocol)

Here is a brief documentation on explaning what;s about and how to run the code, for more details explanation about our design choices, please refer to the engineering_notebook.md

### Download
Run the following command in your terminal to save the repository in your system
> $ git clone https://github.com/wan19990901/CS262.git

Then install the necssary dependecy, which is just pytest

> $ pip install -r requirment.txt


### Run
Once you are in the directory where `server.py` or `client.py` file exists, run by typing the following commands in your terminal.

### Server
> $ python server.py

  
### Client
> $ python client.py 

You can run multiple clients ay the same time by creating multiple processes. 

### Wire Protocol:


Op '0' = Account Login, e.g. 0|wayne123 --> User with ID wayne123 logged in (need to be created at first)

Op '1' = Account Creation, e.g. 1|John --> Creates an account with username John, and an ID will be supplemented. (Avoid same user name, and such format has to be followed and try to aviod adding '|' in the name)

Op '2' = List User, e.g., 2|J.hn --> returns list of user whose name is J*hn. Or 2 --> Returns list of all users

Op '3'  = Send Message to a particular user, e.g., 3|accountID|message --> Send a new message immediately to another account if online (send to mailbox if the other account is offline)

Op '4' = View underlivered message, e.g. 4|accountID --> View all undelivery message for a user with id accountID when he/she is logged off (will return a note if user does not exist)

Op '5' = Delete Account, e.g. 5|accountID --> Delete Account with accountID (will return a note if user does not exist)

Op 'bye' = Logged off. Similar to delete account but the information is kept in the server so that people can still message you in the mailbox, and you can use Op '0' to relogin.

### Test

In the test folder, first run the server scripts:

> $ bash server.sh

Then run the test scipts which creates two clients and run multiple pre-defined instrucitons, and saved results in the output.txt files

> $ bash test.sh

Finally, run pytest on the test.py

> $ pytest test.py

Note that if you can the pre-defined instrucitons on client1/2.sh, you also need to change the tests on test.py to make it right.

You can also run the command to time the test scripts

> $ bash time.sh

This will output a file called time.txt, which will be used for performance comparison with the gRPC counterparts.

Note that you should not run pytest after time, or you need to restart the server.

### Example
For server and client running on the same system

Note that You do not have to interact with the server, the message below are just automatic feedback based on the client's input. You can also refer the feedback to get an idea on the order of input of two clients if you want to replicate this work.

**Server**
> $ python server.py
<pre>
				SERVER WORKING 
socket binded to port 2023
socket is listening
Connected to : 127.0.0.1 : 49032
Connected to : 127.0.0.1 : 49034
1|wayne

Opcode:1
New User created. key: wayne123

1|mason

Opcode:1
New User created. key: mason123

2|w.yne

Opcode:2
key: w.yne

Account matched: wayne

2|.ason

Opcode:2
key: .ason

Account matched: mason

3|wayne|hello

Opcode:3
Sender mason sends a new message hello to wayne

5|mason123

Opcode:5
Account ID: mason123 has been deleted

4|wayne123

Opcode:4
3|mason123|hello too!

Opcode:3
Receiver doesnt exist: mason123

5|wayne1234

Opcode:5
wayne has logged out of the system
</pre>



**Client 1**
> $ python client.py 

<pre>
To get started on this chat room, please create or login your account first and type command as instructed in the documentation 

1|mason
Success New Account Creation! Your new Account ID: mason123


2|.ason
Account matched: mason


3|wayne|hello
Sender mason sends a new message hello to wayne


5|mason123
Your account has been deleted


bye
</pre>

**Client 2**
> $ python client.py 
<pre>
To get started on this chat room, please create or login your account first and type command as instructed in the documentation 

1|wayne
Success New Account Creation! Your new Account ID: wayne123


2|w.yne
Account matched: wayne


mason: hello
4|wayne123
No new messages


3|mason123|hello too!
Receiver: mason123 doesn't exist 


5|wayne1234
User Not Found! 

bye
</pre>

## Second Implementation (gRPC)



### Download

First cd into the grpc directory Then install the necssary dependecy

> $ pip install -r requirment.txt

Then to generate necessary python files, run the following command under the grpc directory 

> $ python3 -m grpc_tools.protoc -Iprotos --python_out=. --grpc_python_out=. protos/chatservice.proto

### Run
Once you are in the directory where `chatservice_pb2_grpc.py` and `chatservice_pb2.py` file exist, run by typing the following commands in your terminal.

### Server
> $ python3 chatservice_server.py
  
### Client
> $ python3 chatservice_client.py

You can run multiple clients ay the same time by creating multiple processes. 

### Wire Protocol:

Op '0' = Account Login, e.g. 0|wayne --> User with ID wayne logged in (need to be created at first)

Op '1' = Account Creation, e.g. 1|John --> Creates an account with username John

Op '2' = List User, e.g., 2|J.hn --> returns list of user whose name is J*hn

Op '3'  = Send Message to a particular user, e.g., 3|accountID|message --> Send a new message immediately to another account if online (send to mailbox if the other account is offline)

All messages that are received during log off will be prompted once the user log in 

Op '5' = Delete Account, e.g. 5| --> Delete Account and quit the client from the chat service

Op 'X' = Logged off. Similar to delete account but the information is kept in the server so that people can still message you, and you can use '0' to relogin.

### Example
For server and client running on the same system

Note that You do not have to interact with the server, the message below are just automatic feedback based on the client's input. You can also refer the feedback to get an idea on the order of input of two clients if you want to replicate this work.

**Server**
> $ python3 chatservice_server.py

INFO:root:Starting server on [::]:50051



**Client 1**
> $ python client.py 

Welcome to the chatroom! Please log into your account by 0 or create a new account by 1.

1|wayne

Account wayne has been created!

2|w.yne

Account matched: wayne

3|mason|hello

Recipient is not found!

5|

Your account has been deleted!

**Client 2**
> $ python client.py 

Welcome to the chatroom! Please log into your account by 0 or create a new account by 1.

1|mason

Account mason has been created!

X

You have been successfully logged out!

> $ python client.py 

Welcome to the chatroom! Please log into your account by 0 or create a new account by 1.

1|wayne

Account wayne has been created!

3|mason|hello

Your message has been sent!

3|mason|hey

Your message has been sent!

x

Invalid request, please try again!

X

You have been successfully logged out!

> $ python client.py 

Welcome to the chatroom! Please log into your account by 0 or create a new account by 1.

0|mason

wayne: hello

wayne: hey

You have been successfully logged in!

5|

Your account has been deleted!