# python-grpc-chat-service
A simple chat service to illustrate a web-sockets like setup using gRPC (underlying HTTP/2)

## Detailed walkthrough
[Create a real-time chat service using gRPC in Python](https://medium.com/@iamdeepaksinghh/create-a-real-time-chat-service-using-grpc-in-python-fc63127d570c)

# Details
The service has the following features -

* chat capability between two parties, send messages and receive messages as soon as they are sent
* receive undelivered messages as soon as a client comes online


A gRPC server is created to which multiple clients can connect. The server is an async one (using async queue). The client uses two threads, one each for sending messages and receiving messages. The receiving messages is achieved by establishing a server-streaming procedure to establish a long-lived connection. The sending messages is achieved using individual requests.

![Architecture](https://i.imgur.com/mHvZgYT.png)
