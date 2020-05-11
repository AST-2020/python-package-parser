class Fehler:

    dateipfad = ''
    zeilennummer = 0
    description = ''

    #Konstruktur initialisieren
    def __init__(self, dateipfad, zeilennummer, description):
        self.dateipfad = dateipfad
        self.zeilennummer = zeilennummer
        self.description = description

    def getDateipfad(self):
        return self.dateipfad

    def getZeilennummer(self):
        return self.zeilennummer

    def getDescription(self):
        return self.description