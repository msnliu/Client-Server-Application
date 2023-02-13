# cs262-WP

Server-side code
To run the server:
  python3 mt-server.py
  
To run the client:
  python3 mt-client.py

Wire Protocol:
Op '1' = Account Creation, e.g. 1|John --> returns accountID \n
Op '2' = Deposit, e.g., 2|accountID|Amount --> returns updated balance\n
Op '3'  = Withdrawal, e.g., 3|accountID|Amount --> returns updated balance\n
Op '4' = View Balance, e.g. 4|accountID --> returns balance\n
