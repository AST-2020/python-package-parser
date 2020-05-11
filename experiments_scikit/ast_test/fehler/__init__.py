class _init_: #Fehler Manager -> Hier muessen alle Fehler die mit der Klasse Fehler registriert werden

    fehler = []

    def __init__(self, fehler):
        self.fehler[len(fehler)] = fehler

    #Fehler wird der Liste hinzugefuegt
    def fehlerHinzufuegen(self, Fehler):
        self.fehler.append(Fehler)

    def fehlerLoeschen(self, Fehler):
        self.fehler.remove(Fehler)

    def printFehler(self):
        print(self.fehler)