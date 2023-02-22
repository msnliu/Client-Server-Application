import logging
from asyncio import Queue
from typing import Dict


class MessageQueue:

    topics: Dict[str, Queue] = {}

    def get_message_offset(self, recipient_id):
        recipient_queue = self.get_or_create_queue(recipient_id)
        return recipient_queue.qsize()

    async def put_message(self, recipient_id, message_object):
        recipient_queue = self.get_or_create_queue(recipient_id)
        message_id = recipient_queue.qsize()
        await recipient_queue.put(message_object)
        logging.info(f"Message inserted in queue for recipient={recipient_id}")
        return message_id

    async def get_message(self, recipient_id):
        recipient_queue = self.get_or_create_queue(recipient_id)
        logging.info(f"Reading from queue for recipient={recipient_id}")
        unread_message = await recipient_queue.get()
        logging.info(f"Received new message for recipient={recipient_id}")
        return unread_message

    def get_or_create_queue(self, recipient_id):
        if not self.topics.get(recipient_id):
            self.topics[recipient_id] = Queue()
        return self.topics[recipient_id]
