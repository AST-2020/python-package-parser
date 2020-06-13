class Message:
    def __init__(self, dateipfad, zeilennummer, description, dateiname):
        self.dateipfad = dateipfad
        self.zeilennummer = zeilennummer
        self.description = description
        self.dateiname = dateiname

    def __str__(self):
        return "error occured  in [" + self.dateipfad + " in file " + self.dateiname + "] in line " + str(
            self.zeilennummer) + ": " + self.description


class MessageManager:
    def __init__(self, message=None):
        if message is None:
            message = []

        self.message = message

    def add_message(self, message):
        self.message.append(message)

    def print_messages(self):
        for f in self.message:
            print(f)
            print("----")
