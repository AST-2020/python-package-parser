class Fehler:
    def __init__(self, dateipfad, zeilennummer, description, dateiname):
        self.dateipfad = dateipfad
        self.zeilennummer = zeilennummer
        self.description = description
        self.dateiname = dateiname

    def __str__(self):
        return "error occured  in [" + self.dateipfad + " in file " + self.dateiname + "] in line " + str(
            self.zeilennummer) + ": " + self.description


class FehlerManager:
    # Fehler Manager -> Hier muessen alle Fehler die mit der Klasse Fehler registriert werden

    # Wenn man moechte, kann man eine Liste mit fehlern uebergeben, ansonsten wird eine erzeugt.
    def __init__(self, fehler=None):
        if fehler is None:
            fehler = []

        self.fehler = fehler

    # Fehler wird der Liste hinzugefuegt
    def fehlerHinzufuegen(self, Fehler):
        self.fehler.append(Fehler)
        # print("Fehler wurde hinzugefuegt")

    def fehlerLoeschen(self, Fehler):
        self.fehler.remove(Fehler)
        print("Fehler wurde entfernt")

    def printFehlerList(self):
        for f in self.fehler:
            print(f)
            print("----")
