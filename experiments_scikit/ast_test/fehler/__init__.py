class Fehler:

    dateipfad = ''
    zeilennummer = 0
    description = ''

    # Konstruktur initialisieren
    def __init__(self, dateipfad, zeilennummer, description):
        self.dateipfad = dateipfad
        self.zeilennummer = zeilennummer
        self.description = description

class FehlerManager:
#Fehler Manager -> Hier muessen alle Fehler die mit der Klasse Fehler registriert werden

    fehler = []

    #Fehler wird der Liste hinzugefuegt
    def fehlerHinzufuegen(self, Fehler):
        self.fehler.append(Fehler)
        print("Fehler wurde hinzugefuegt")

    def fehlerLoeschen(self, Fehler):
        self.fehler.remove(Fehler)
        print("Fehler wurde entfernt")

    def printFehler(self):
        for f in self.fehler:
            print(f.dateipfad)
            print(f.zeilennummer)
            print(f.description)

    def main(self):
        fehler1 = Fehler("test", 12, "test2")
        self.fehlerHinzufuegen(fehler1)
        self.printFehler()
        self.fehlerLoeschen(fehler1)

    if __name__ == '__main__':
        main()