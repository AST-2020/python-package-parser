from typing import List

from analysis.message import Message


class MessageManager:
    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def print_messages(self):
        for message in sorted(self.messages, key=lambda msg: msg.location):
            print(message)
