from typing import List

from analysis.message import Message


class MessageManager:
    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def print_messages(self):
        sorted_messages = sorted(self.messages, key=lambda msg: msg.location)
        for message in sorted_messages:
            print(message)
