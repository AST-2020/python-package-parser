import car

myCar = car.Car("Toyota", "Supra", "red")
myCar = car.Car(make="VW", modell="Golf", color="blue")

myCar.get_info()
myCar.get_info(haha=10)
myCar.gett_info()
myCar.drive(speed=50)
myCar.drive(speed=150)
myCar.drive(speed=200, bla=1)
myCar.drive(sped=15)

car.play_music(song_name="Deja Vu", artist="Dave Rodgers")
car.play_music(song_name="Enter Sandman", artisst="Metallica")
