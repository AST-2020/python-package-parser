class Car():
    # This is a custom class to test Marwin's code
    # The car has attributes like the make, model and color

    def __init__(self, make, model, color):
        self.make = make
        self.model = model
        self.color = color

    # !! IMPORTANT !!
    # Since the "print()" function causes problems with the parser code,
    # these functions don't return a value but print the information directly.
    def drive(self, speed):
        if (speed > 100):
            print("Vrooooooooooom stututu")
        else:
            print("vroom")

    def get_info(self):
        print("I have a " + self.color + " " + self.make + " " + self.model)

def play_music(song_name, artist):
    print("Playing " + song_name + " by " + artist)