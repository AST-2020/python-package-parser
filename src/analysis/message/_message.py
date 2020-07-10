from user_code.model import Location


class Message:
    def __init__(self, location: Location, description: str, iswarning = False):
        self.location: Location = location
        self.description: str = description
        self.iswarning = iswarning
    def __str__(self):
        if self.iswarning == True:
            return f"Warning in {self.location}: {self.description}"
        return f"Error in {self.location}: {self.description}"
