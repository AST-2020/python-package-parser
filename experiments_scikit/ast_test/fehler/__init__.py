from experiments_scikit.ast_test.fehler import Fehler

class _init_: #Fehler Manager -> Hier muessen alle Fehler die mit der Klasse Fehler registriert werden

    fehler = []

    def __init__(self, fehler):
        self.fehler[len(fehler)] = fehler

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
