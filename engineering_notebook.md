Author: Guangya Wan & Zongjun Liu
Note: No | in the input besides for supporting different arguments

# Custom Wire Proctol
## Client 


The code imports the following modules:
threading : A module to create and manage threads.
socket : A module to create a socket object.
time : A module to add delays.
sys : A module providing access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter.
Defining the Main Function

The main function is defined as Main().
It initializes the host address and port number to connect with the server.
Creates a socket object with AF_INET and SOCK_STREAM as its parameters.
Connects to the server using the connect() method of the socket object.
Defines two functions sender() and receiver() for sending and receiving messages from the server.
Defining the Sender Function

This function is responsible for sending messages to the server.
It runs in an infinite loop and takes user input as the message.
It then sends the message to the server using the send() method of the socket object.
It adds a small delay using time.sleep() to avoid overloading the server with messages.
If the user input is 'bye' or 'quit', it breaks the loop and shuts down the socket for writing using s.shutdown().
If the user input is anything else, it continues the loop.
Defining the Receiver Function

This function is responsible for receiving messages from the server.
It runs in an infinite loop and receives messages using the recv() method of the socket object.
It then prints the received message on the console using the print() function.
If the received message is empty, it shuts down the socket for reading and exits the loop.
Creating Threads

Two threads are created using the Thread() method of the threading module.
One thread is for the sender function, and the other is for the receiver function.
Starting Threads

The threads are started using the start() method of the thread object.
Joining Threads

The threads are joined using the join() method of the thread object.
Closing the Socket

The socket is closed using the close() method of the socket object.
Executing the Program

The program is executed only if the script is run as the main module using the __name__ variable.




## Server

The User class stores user details such as their name, ID, and an empty message queue queue. The Server class is the main class that creates and manages the chat server. It has several functions including start_server, account_creation, list_accounts, send_message, pop_undelivered, delete_account, and close_server.

The start_server function initializes the server and sets it to listen to incoming connections. The close_server function closes the server. The account_creation function creates a new user account and adds it to the server's account table. The list_accounts function searches for existing user accounts based on a pattern. The send_message function sends a message from one user to another. The pop_undelivered function checks and retrieves any undelivered messages in a user's queue. The delete_account function deletes a user account.

The err_msg variable is used to display error messages for invalid input.

The numpy library is imported but is not used in the code.

The code also imports the socket, re, and _thread libraries. The socket library is used for creating and managing the sockets. The _thread library is used for creating and managing threads. The re library is used for handling regular expressions.

## testing

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