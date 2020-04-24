"""
Dictonary

Idee:
    Dict
        -   class: name
        -   functions: Dict of functions
                -   function:   name
                -   parameters: dict of params
                        -   parameter:  name

Unklar, wie kann man itterativ nested dicts erstellt, hinzufuegt

"""


class Dict:
    def __init__(self):
        self.classes = {}

    def addClass(self, cls):
        self.classes[cls] = {}

    def addFunction(self, func, cls):
        self.classes[cls][func] = {}
        self.classes[cls][func]['params'] = []

    def addParam2Function(self, param, func, cls):
        # ToDo spaeter erweiterung, durch dict statt list, um typen mit zu speichern
        self.classes[cls][func]['params'].append(param)



"""if __name__ == '__main__':
    dict = Dict()
    dict.addClass('SVC')
    dict.addFunction('get', 'SVC')
    dict.addParam2Function('var', 'get', 'SVC')
    dict.addFunction('set', 'SVC')
    dict.addParam2Function('var', 'set', 'SVC')
    dict.addParam2Function('var2', 'set', 'SVC')

    print(dict.classes)"""
