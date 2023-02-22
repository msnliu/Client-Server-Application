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
If the user input is 'bye' or 'quit', it breaks the loop and shuts down the socket for writing using s.shutdown().
If the user input is anything else, it continues the loop.
Receiver Function:

This function is responsible for receiving messages from the server.
It runs in an infinite loop and receives messages using the recv() method of the socket object.
It then prints the received message on the console using the print() function.
If the received message is empty, it shuts down the socket for reading and exits the loop.
Threads:

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

## testing