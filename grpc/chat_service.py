import logging
from chatservice_pb2 import (
    ChatMessageRequest,
    ChatMessageResponse,
    ChatMessage,
    ChatClient,
)
from message_queue import MessageQueue


class ChatService:
    message_queue: MessageQueue = MessageQueue()

    async def write_message(self, request: ChatMessageRequest) -> ChatMessageResponse:
        recipient_id = request.recipient_id
        message_id = self.message_queue.get_message_offset(recipient_id)
        message_id = await self.message_queue.put_message(
            recipient_id=recipient_id,
            message_object=ChatMessage(
                id=message_id,
                thread_id=request.thread_id,
                message=request.message,
                sender_id=request.sender_id,
                recipient_id=recipient_id,
            ),
        )
        return ChatMessageResponse(id=message_id)

    async def read_next_message(self, request: ChatClient) -> ChatMessage:
        return await self.message_queue.get_message(request.recipient_id)
