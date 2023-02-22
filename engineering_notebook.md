Author: Guangya Wan & Zongjun Liu
Note: No | in the input besides for supporting different arguments

# Custom Wire Proctol
## Client 

### Summary

## Server

### Summary

The User class stores user details such as their name, ID, and an empty message queue queue. The Server class is the main class that creates and manages the chat server. It has several functions including start_server, account_creation, list_accounts, send_message, pop_undelivered, delete_account, and close_server.

The start_server function initializes the server and sets it to listen to incoming connections. The close_server function closes the server. The account_creation function creates a new user account and adds it to the server's account table. The list_accounts function searches for existing user accounts based on a pattern. The send_message function sends a message from one user to another. The pop_undelivered function checks and retrieves any undelivered messages in a user's queue. The delete_account function deletes a user account.

The err_msg variable is used to display error messages for invalid input.

The numpy library is imported but is not used in the code.

The code also imports the socket, re, and _thread libraries. The socket library is used for creating and managing the sockets. The _thread library is used for creating and managing threads. The re library is used for handling regular expressions.