Author: Guangya Wan & Zongjun Liu
Note: No | in the input besides for supporting different arguments

# Custom Wire Proctol

For simplicity, for all the client and server code below, the default host  is  "127.0.0.1" and the default port is 2023. And 
## Client 
The Client code imports the following modules:
threading : A module to create and manage threads.
socket : A module to create a socket object.
time : A module to add delays.
sys : A module providing access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.

The main function is defined as Main().
It initializes the host address and port number to connect with the server.
Creates a socket object with AF_INET and SOCK_STREAM (Since IP4 is used) as its parameters.
Connects to the server using the connect() method of the socket object.
Defines two functions sender() and receiver() for sending and receiving messages from the server.
Sender Function:

This function is responsible for sending messages to the server.
It runs in an infinite loop and takes user input as the message.
It then sends the message to the server using the send() method of the socket object.
It adds a small delay using time.sleep() to avoid overloading the server with messages.
If the user input is 'bye', it breaks the loop and shuts down the socket for writing using s.shutdown().
If the user input is anything else, it continues the loop.
Receiver Function:

This function is responsible for receiving messages from the server.
It runs in an infinite loop and receives messages using the recv() method of the socket object.
It then prints the received message on the console using the print() function.
If the received message is empty, it shuts down the socket for reading and exits the loop.
Threads:

Two threads are created using the Thread() method of the threading module.
One thread is for the sender function, and the other is for the receiver function.

The threads are started using the start() method of the thread object.

The threads are joined using the join() method of the thread object.

The socket is closed using the close() method of the socket object.

The program is executed only if the script is run as the main module using the __name__ variable.

Note that there are multiples ways to implement the muti-clients setting. Another widely used option is to use the select module; we didn't try it here as that was more complex and the threading module here is sufficient for our application.

## Server

We created a User class which stores user details such as their name, ID(Note here, we have both ID and name, and this is design choice; you can view ID as an password for security purpose, e.g people can not delete or checck undeliveryed message without knowing the ID), and an empty message queue (for storing the undeliervered message). The Server class is the main class that creates and manages the chat server. It has several functions including start_server, account_creation, list_accounts, send_message, pop_undelivered, delete_account, and close_server.

The following is a brief summary of the methods in the class:

__init__: Initializes the server by setting up the instance variables.
start_server: Starts the server by creating a socket and listening for incoming connections. Once a connection is established, a new thread is created to handle the communication with the client.
close_server: Closes the server.
account_creation: Creates a new user account and assigns a unique ID to the account. The account is added to the accountName_table dictionary, and the connection is added to the connections and connections_id dictionaries.
list_accounts: Takes a pattern as an input and returns a list of accounts that match the pattern.
send_message: Sends a message from one user to another.
pop_undelivered: Retrieves any undelivered messages for a specific user.
delete_account: Deletes a user account.
The start_server method runs in an infinite loop until the server is closed. It listens for incoming connections using the socket module and creates a new thread to handle each client's communication with the server.

The account_creation method creates a new user account and assigns a unique ID to the account. The account is added to the accountName_table dictionary, and the connection is added to the connections and connections_id dictionaries.

The list_accounts method takes a pattern as an input and returns a list of accounts that match the pattern. The method searches for the pattern in the accountName_table dictionary and returns the list of matching accounts.

The send_message method sends a message from one user to another. The method takes the name of the recipient and the message as inputs, searches for the recipient's ID in the accountName_table dictionary, and sends the message to the recipient if they are online. If the recipient is offline, the message is added to their mailbox.

The pop_undelivered method retrieves any undelivered messages for a specific user. The method takes the user's ID as input, retrieves the user's mailbox from the accountName_table dictionary, and returns the list of undelivered messages.

The delete_account method deletes a user account. The method takes the user's ID as input, removes the account from the accountName_table dictionary, and removes the user's connection from the connections and connections_id dictionaries. If there are any undelivered messages in the user's mailbox, the method prompts the user to check their mailbox before deleting the account.

This core of the server lies on the function threaded(self, c) which is used to manage the communication with a client in a threaded way(so client can send message to other clients and receive messages from the severs at the same time). The method receives a client socket connection object c as an argument, which is used to communicate with the client.

The method first sets up an empty list to store received data and then receives data from the client using the recv method of the socket connection object. The received data is then decoded from bytes to a UTF-8 string using the decode method.

If no data is received, it checks if the connection is in the connections_id dictionary, which maps connections to user IDs. If it is, it gets the user associated with the connection, sets their active attribute to False, and prints a log message indicating that the user has logged out. If the connection is not in the dictionary, the method simply breaks the loop and exits.

If data is received, it is printed to the console. The data is then split on the | character and the resulting list is stored in data_list. The first element of the list is extracted and stored in the opcode variable.

If the opcode is 0, the method attempts to log in the user by checking if the second element of data_list (which is assumed to be the user ID) is in the accountName_table dictionary. If it is, the associated User object is retrieved and its active attribute is set to True. The connection is added to the connections dictionary under the user's ID, and the connection is added to the connections_id dictionary with the user's ID as the value. A log message indicating that the user has logged in is printed to the console, and a response message is sent back to the client.

If the opcode is 1, the method attempts to create a new account by calling the account_creation method with the second element of data_list as the argument. The response from account_creation is then sent back to the client.

If the opcode is 2, the method either lists all account names (if the length of data_list is 1) or lists the accounts associated with a specific user ID (if the second element of data_list is a user ID). The response from the list_accounts method is then sent back to the client.

If the opcode is 3, the method attempts to send a message to a recipient by calling the send_message method with the second and third elements of data_list as arguments. The response from send_message is then sent back to the client.

If the opcode is 4, the method attempts to retrieve any undelivered messages for a specific user ID by calling the pop_undelivered method. The response from pop_undelivered is then sent back to the client.

If the opcode is 5, the method attempts to delete an account by calling the delete_account method with the second element of data_list as the argument. The response from delete_account is then sent back to the client.

If the opcode is anything other than 0-5, an error message is sent back to the client. (Note that the cases when opcode = 'bye' or 'quit' is handled in the client side)

## testing (For both base case and gRPC)

The testing invovled the interaction between client and server.
the server.sh is responsible for starting the server
the three clients shell scipts involved pre-defined behaviors of clients (covers all functionality we proposed); the feedback to the clients were then saved in the output.txt for automated check in pytest on the test_base.py file
We also tested the performance of this code by running the time.sh scripts. It's fair to compare in this way since they all accomplish same behavior. The result is then further saved in time.txt file for both folder.

# gRPC

## Client 

### Overview
This notebook describes the implementation of a chat client in Python using the gRPC framework to interact with a chat server. The chat client allows users to create a new account, log into an existing account, send and receive chat messages, and delete their account.

The client is implemented with two threads: a read handler and a write handler. The read handler listens for incoming messages from other clients and prints them to the console. The write handler listens for input from the user and sends messages to other clients or performs other operations based on the user's input. Using threading helps to prevent the program from blocking while waiting for input or messages from the server.

### Code Structure

The code is organized into the following functions:

#### run()

This is the main function of the chat client. It establishes a connection to the chat server, prompts the user to log in or create a new account, and starts the read_handler and write_handler threads.

#### read_handler(client_id, stub)

This function is run in a separate thread and listens for new chat messages from the server. When a new message is received, it is displayed to the user.

#### write_handler(client_id, stub)

This function is run in a separate thread and reads user input from the console. It then sends the input to the server to be processed.

### gRPC API

The chat client uses the following gRPC API methods:

#### LogIn(LogInRequest)

Logs a user into an existing account.

#### LogOut(LogOutRequest)

Logs a user out of their account.

#### CreateAccount(CreateAccountRequest)

Creates a new account for a user.

#### DeleteAccount(DeleteAccountRequest)

Deletes a user's account.

#### SendMessage(ChatMessageRequest)

Sends a chat message to another user.

#### ReceiveMessages(ChatClient)

Receives chat messages sent to the user.

#### WildCard(WildCardRequest)

Sends a wildcard message to the server.

### Input and Output Format

The chat client expects user input to be in the following format:

{option code}|{data}

The following option codes are supported:

0: Log in to an existing account.

1: Create a new account.

2: Send a wildcard message to the server.

3: Send a chat message to another user.

5: Delete the user's account.

The 2 option code is used to send a wildcard message to the server. A wildcard message is a special message that the server can use to respond to multiple clients at once.

The 3 option code is used to send a chat message to another user. The data parameter should be in the following format:

{recipient_id}|{message}

The recipient_id parameter is the ID of the user that the message is being sent to.

The chat client outputs messages received from the server to the console in the following format:

{sender_id}: {message}

If the message was sent by the server, the sender_id field will be set to "Server".

Dependencies

The chat client depends on the following Python packages:

#### grpc

#### chatservice_pb2

#### chatservice_pb2_grpc

#### logging

#### threading

## Server

### Design
The code has two main classes: ChatClient and ChatService. ChatClient represents a client, and ChatService represents the server. The Server class implements the ChatServiceServicer interface and handles client requests.

The ChatService class manages messages sent and received. It has methods to add a new message to a conversation, read the next message from a conversation, and get all messages in a conversation.

The ChatClient class has attributes to store client information such as the client ID and online status.

The Server class has methods to create an account, delete an account, send a message, receive messages, and search for clients using wildcard patterns.

The main function starts a gRPC server, and listens on port 50051. It waits for incoming requests, and when a request is received, it forwards the request to the appropriate method in the Server class.

### Implementation
The implementation of the code uses Python's asyncio and grpc libraries. The asyncio library provides asynchronous programming support, and the grpc library provides gRPC implementation in Python.

The implementation of the code is organized into several Python modules:

#### chatservice_pb2.py - defines the protobuf messages that the service uses for communication.

#### chatservice_pb2_grpc.py - defines the gRPC service and its methods.

#### chat_service.py - defines the ChatService class for managing messages.

#### chat_client.py - defines the ChatClient class for client information.

#### server.py - defines the Server class and implements the gRPC service methods.

#### client.py - defines the client class for sending and receiving messages.

The code uses the async and await keywords to perform asynchronous programming. Asynchronous programming is useful when multiple I/O bound tasks need to be performed simultaneously, as it allows the program to continue executing while the I/O operation is being performed.

### Testing
To test the code, I ran the server.py file to start the gRPC server, and then ran the client.py file to interact with the server. The client.py file simulates two clients, sending and receiving messages, and creating and deleting accounts.

I also used the grpc_cli command-line tool to test the gRPC service. The grpc_cli tool provides a command-line interface for making gRPC requests. I used it to send requests to the server and verify that the responses were correct.

### Conclusion
In conclusion, the code provides a basic implementation of a chat service using gRPC and asyncio. It uses the ChatService class to manage messages, and the Server class to handle client requests. The implementation uses asynchronous programming to allow the program to continue executing while I/O bound tasks are being performed. The code was tested using the client.py file and the grpc_cli command-line tool.

# Comparison

gRPC and Custom Wire Protocol both have their advantages and disadvantages when it comes to complexity, performance, and buffer size.

In terms of complexity, gRPC provides a high-level API for building distributed systems. It abstracts away many of the details of building distributed systems, including connection management, load balancing, and service discovery. This makes it easier to build distributed systems, but it can also make it harder to understand what is happening under the hood.

On the other hand, building a custom wire protocol using sockets and threads requires more low-level programming. Developers need to manage connections, message framing, and error handling themselves. This can result in more code and a steeper learning curve, but it also gives developers more control and a deeper understanding of what is happening in the system.

In terms of performance, gRPC is designed to be fast and efficient. It uses binary serialization and compression to reduce the size of messages being sent between the client and server, and it uses HTTP/2 to multiplex requests and responses over a single connection. This can result in better performance (real time 0.7s) and lower latency than a custom wire protocol (real time 1.7s) implemented using sockets and threads.

However, it is worth noting that a well-designed custom wire protocol can also be very performant. By carefully managing message framing and using efficient serialization and compression techniques, developers can achieve good performance with a custom wire protocol.

Finally, when it comes to buffer size, gRPC has some advantages over a custom wire protocol. Because gRPC uses binary serialization and compression, it can often send smaller messages between the client and server. This can be particularly important in low-bandwidth environments, where every byte counts.

However, it is also worth noting that a well-designed custom wire protocol can also be efficient with buffer size. By using efficient message framing and compression techniques, developers can reduce the size of messages being sent over the wire.

In summary, gRPC and custom wire protocols each have their own strengths and weaknesses when it comes to complexity, performance, and buffer size. While gRPC is generally easier to use and can be more performant, a custom wire protocol can offer more control and be just as performant when implemented correctly. Ultimately, the choice between gRPC and a custom wire protocol will depend on the specific requirements of the system being built.
