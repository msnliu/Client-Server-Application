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