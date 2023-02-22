import asyncio
import grpc
import logging
import re

from typing import Dict

from chatservice_pb2_grpc import ChatServiceServicer, add_ChatServiceServicer_to_server
from chatservice_pb2 import (
    CreateAccountRequest,
    CreateAccountResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    WildCardRequest,
    WildCardResponse,
    LogInRequest,
    LogInResponse,
    LogOutRequest,
    LogOutResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    ChatMessage,
    ChatClient,
)
from chat_service import ChatService
from chat_client import ChatClient


class Server(ChatServiceServicer):
    chat_service: ChatService = ChatService()
    clients: Dict[str, ChatClient] = {}

    async def SendMessage(
        self, request: ChatMessageRequest, context: grpc.aio.ServicerContext
    ) -> ChatMessageResponse:
        logging.info(f"SendMessage called with {request=}")
        if request.recipient_id in self.clients.keys():
            await self.chat_service.write_message(request)
            msg = "Your message has been sent!"
        else:
            msg = "Recipient is not found!"
        request2 = ChatMessageRequest(
            thread_id=1,
            message=msg,
            sender_id="Server",
            recipient_id=request.sender_id,
        )
        await self.chat_service.write_message(request2)
        return ChatMessageResponse()

    async def ReceiveMessages(
        self, request: ChatClient, context: grpc.aio.ServicerContext
    ) -> ChatMessage:
        logging.info(f"ReceiveMessages called with {request=}")
        while self.is_online(request.recipient_id):
            message_object = await self.chat_service.read_next_message(request)
            yield message_object

    async def CreateAccount(
        self, request: CreateAccountRequest, context: grpc.aio.ServicerContext
    ) -> CreateAccountResponse:
        logging.info(f"CreateAccount called with {request=}")       
        client_id = request.client_id
        self.clients[client_id] = ChatClient(client_id)
        msg = "Account " + client_id + " has been created!"
        request2 = ChatMessageRequest(
            thread_id=1,
            message=msg,
            sender_id="Server",
            recipient_id=request.client_id,
        )
        await self.chat_service.write_message(request2)
        return CreateAccountResponse()

    async def DeleteAccount(
        self, request: DeleteAccountRequest, context: grpc.aio.ServicerContext
    ) -> CreateAccountResponse:
        logging.info(f"CreateAccount called with {request=}")       
        client_id = request.client_id
        del self.clients[client_id]
        msg = "Your account has been deleted!"
        request2 = ChatMessageRequest(
            thread_id=1,
            message=msg,
            sender_id="Server",
            recipient_id=request.client_id,
        )
        await self.chat_service.write_message(request2)
        return DeleteAccountResponse()
    
    async def WildCard(
        self, request: WildCardRequest, context: grpc.aio.ServicerContext
    ) -> WildCardResponse:
        logging.info(f"WildCard called with {request=}")  
        pattern = request.pattern
        match = "^" + pattern + "$"
        regex = re.compile(match)
        matches = [string for string in self.clients.keys() if re.match(regex, string)]
        if len(matches):
            msg = "Account matched: " + ','.join(matches)
        else:
            msg = "Account matched to: " + str(pattern)  + " doesn't exist"
        request2 = ChatMessageRequest(
            thread_id=1,
            message=msg,
            sender_id="Server",
            recipient_id=request.client_id,
        )
        await self.chat_service.write_message(request2)
        return WildCardResponse()

    async def LogIn(
        self, request: LogInRequest, context: grpc.aio.ServicerContext
    ) -> LogInResponse: 
        client_id = request.client_id
        logging.info(f"messenger={client_id} going online.")
        if client_id in self.clients.keys():
            self.clients[client_id].set_online(True)
            msg = "You have been successfully logged in!"
            request2 = ChatMessageRequest(
                thread_id=1,
                message=msg,
                sender_id="Server",
                recipient_id=request.client_id,
            )
        await self.chat_service.write_message(request2)
        return LogInResponse()

    async def LogOut(
        self, request: LogOutRequest, context: grpc.aio.ServicerContext
    ) -> LogOutResponse: 
        client_id = request.client_id
        logging.info(f"messenger={client_id} going offline.")
        self.clients[client_id].set_online(False)
        msg = "You have been successfully logged out!"
        request2 = ChatMessageRequest(
            thread_id=1,
            message=msg,
            sender_id="Server",
            recipient_id=request.client_id,
        )
        await self.chat_service.write_message(request2)
        return LogOutResponse()

    def is_online(self, client_id):
        if client_id not in self.clients.keys():
            return False
        return self.clients[client_id].is_online()

async def serve() -> None:
    server = grpc.aio.server()
    add_ChatServiceServicer_to_server(Server(), server)
    listen_addr = "[::]:50051"
    server.add_insecure_port(listen_addr)
    logging.info(f"Starting server on {listen_addr}")

    await server.start()  
    await server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        print("\nServer stopped by KeyboardInterrupt")
