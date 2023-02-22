# cs262-HW1 Guangya Wan & Zongjun Liu

## About
This code implements a chat server using socket programming in Python with multi-threading. It allows the creation of new user accounts, searching for existing accounts, sending messages to other users, and deleting user accounts. The chat server is capable of handling multiple clients at the same time. Two methods(custom wire proctol and gRPC) were implemented 

## First Implementation (Custom Wire Protocol)

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
> $ python client.py hostname

You can run multiple clients ay the same time by creating multiple processes. 

### Wire Protocol:

Op '0' = Account Login, e.g. 0|123 --> returns accountID 

Op '1' = Account Creation, e.g. 1|John --> returns accountID 


Op '2' = Deposit, e.g., 2|accountID|Amount --> returns updated balance


Op '3'  = Withdrawal, e.g., 3|accountID|Amount --> returns updated balance


Op '4' = View Balance, e.g. 4|accountID --> returns balance


#### Example
For server and client running on the same system

**Server**
> $ python server.py
<pre>
				SERVER WORKING 
Client (127.0.0.1, 51638) connected  [ tesla ]
Client (127.0.0.1, 51641) connected  [ albert ]
Client (127.0.0.1, 51641) is offline  [ albert ]
</pre>



**Client 1**
> $ python client.py localhost

<pre>
CREATING NEW ID:
Enter username: tesla
Welcome to chat room. Enter 'tata' anytime to exit
You: Hello
albert joined the conversation 
albert: world
albert left the conversation
You:
</pre>

**Client 2**
> $ python client.py localhost
<pre>
CREATING NEW ID:
Enter username: albert
Welcome to chat room. Enter 'tata' anytime to exit
You: World
You: tata
DISCONNECTED!!
</pre>




