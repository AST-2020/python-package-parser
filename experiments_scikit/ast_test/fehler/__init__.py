class Fehler:

    #Daten werden gespeichert.
    dateipfad = ''
    zeilennummer = 0
    description = ''

    # Konstruktur initialisieren
    def __init__(self, dateipfad, zeilennummer, description):
        self.dateipfad = dateipfad
        self.zeilennummer = zeilennummer
        self.description = description

    def printFehler(self, Fehler):
        print(self.dateipfad)
        print(self.description)
        print(self.zeilennummer)

class FehlerManager:
#Fehler Manager -> Hier muessen alle Fehler die mit der Klasse Fehler registriert werden

    def __init__(self, fehler = []):

        self.fehler = fehler

    #Fehler wird der Liste hinzugefuegt
    def fehlerHinzufuegen(self, Fehler):
        self.fehler.append(Fehler)
        print("Fehler wurde hinzugefuegt")

    def fehlerLoeschen(self, Fehler):
        self.fehler.remove(Fehler)
        print("Fehler wurde entfernt")

    def printFehlerList(self):
        for f in self.fehler:
            print(f.dateipfad)
            print(f.zeilennummer)
            print(f.description)


if __name__ == '__main__':
    fm = FehlerManager()
    fehler1 = Fehler("test", 12, "test2")
    fm.fehlerHinzufuegen(fehler1)
    fm.printFehlerList()
    fm.fehlerLoeschen(fehler1)