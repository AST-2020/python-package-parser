from typing import List

from analyses.messages import Message


class MessageManager:
    def __init__(self):
        self.messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def print_messages(self):
        for f in self.messages:
            print(f)
            print("----")
