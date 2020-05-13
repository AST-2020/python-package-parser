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

    #Einzelne Fehler printen
    def printFehler(self, Fehler):
        print(self.dateipfad + "in Zeile " + self.zeilennummer + " folgender Fehler: " + self.description)
        print("----")

class FehlerManager:
#Fehler Manager -> Hier muessen alle Fehler die mit der Klasse Fehler registriert werden

    #Wenn man moechte, kann man eine Liste mit fehlern uebergeben, ansonsten wird eine erzeugt.
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
            print(self.dateipfad + "in Zeile " + self.zeilennummer + " folgender Fehler: " + self.description)
            print("----")