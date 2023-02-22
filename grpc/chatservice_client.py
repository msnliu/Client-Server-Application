import logging
import threading
import random

import grpc
from chatservice_pb2 import CreateAccountRequest, WildCardRequest, LogInRequest, LogOutRequest, DeleteAccountRequest, ChatMessageRequest, ChatClient
from chatservice_pb2_grpc import ChatServiceStub


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = ChatServiceStub(channel)
        while True:
            user_input = str(input("Welcome to the chatroom! Please log into your account by 0 or create a new account by 1.\n"))
            data_list = user_input.split('|')
            if (len(data_list) == 2) and (data_list[0] in ['0','1']):
                optcode = data_list[0]
                client_id = data_list[1]
                if optcode == '0':
                    stub.LogIn(
                        LogInRequest(
                            client_id = client_id
                        )
                    )
                    break
                elif optcode == '1':
                    stub.CreateAccount(
                        CreateAccountRequest(
                            client_id = client_id
                        )
                    )
                    break
            else:
                print("Invalid request, please try again!")
                continue

        read_thread = threading.Thread(
            target=read_handler,
            args=(
                client_id,
                stub,
            ),
        )
        write_thread = threading.Thread(
            target=write_handler,
            args=(
                client_id,
                stub,
            ),
        )

        write_thread.start()
        read_thread.start()

        write_thread.join()
        read_thread.join()

        print("Quitting!")

def read_handler(client_id, stub):
    read_stream = stub.ReceiveMessages(ChatClient(recipient_id=client_id))
    for response in read_stream:
        if response.sender_id == "Server":
            print(f"\r{response.message}")
        else:
            print(f"\r{response.sender_id}: {response.message}")


def write_handler(client_id, stub):
    while True:
        message = input()
        if message == "":
            stub.LogOut(
                LogOutRequest(
                    client_id = client_id
                )
            )
            break

        data_list = message.split('|')
        optcode = data_list[0]

        if optcode == '2':
            pattern = data_list[1]
            stub.WildCard(
                WildCardRequest(
                    client_id=client_id,
                    pattern=pattern
                )
            )
            
        elif optcode == '3':
            recipient_id = data_list[1]
            message = data_list[2]
            stub.SendMessage(
                ChatMessageRequest(
                    thread_id=1,
                    message=message,
                    sender_id=client_id,
                    recipient_id=recipient_id,
                )
            )

        elif optcode == '5':
            stub.DeleteAccount(
                DeleteAccountRequest(
                    client_id=client_id,
                )
            )
            break
        else:
            print("Invalid request, please try again!")
            continue

if __name__ == "__main__":
    logging.basicConfig()
    run()
