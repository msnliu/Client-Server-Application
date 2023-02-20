# cs262-WP


To run the server:
  python3 mt-server.py
  
To run the client:
  python3 mt-client.py

Wire Protocol:


Op '0' = Account Login, e.g. 0|123 --> returns accountID 

Op '1' = Account Creation, e.g. 1|John --> returns accountID 


Op '2' = Deposit, e.g., 2|accountID|Amount --> returns updated balance


Op '3'  = Withdrawal, e.g., 3|accountID|Amount --> returns updated balance


Op '4' = View Balance, e.g. 4|accountID --> returns balance
