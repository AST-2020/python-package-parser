from user_code.model import Location


class Message:
    def __init__(self, location: Location, description: str):
        self.location: Location = location
        self.description: str = description

    def __str__(self):
        return f"Error in {self.location}: {self.description}"
