class Message:
    def __init__(self, file: str, line: int, description: str):
        self.file: str = file
        self.line: int = line
        self.description: str = description

    def __str__(self):
        return f"Error in '{self.file}' line {self.line}: {self.description}"
