class Message:
    def __init__(self, file: str, line: int, description: str):
        self.file: str = file
        self.line: int = line
        self.description: str = description

    def __str__(self):
        return f"Error in '{self.file}' line {self.line}: {self.description}"


class MessageManager:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def print_messages(self):
        for f in self.messages:
            print(f)
            print("----")
