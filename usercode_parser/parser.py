import ast as ast
from typing import Any
from comparator import Comparator

import torch



class ImportVisitor(ast.NodeVisitor):

    def __init__(self):
        ast.NodeVisitor.__init__(self)
        # to get imported modules
        self.modules = []


    def visit_Import(self, node: ast.Import) -> Any:
        #print(ast.dump(node))
        for alias in node.names:
            self.modules.append(alias.name)


    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        #print(ast.dump(node))
        self.modules.append(node.module)


    def get_list(self, tree):
        # returns a list with all imported modules
        self.visit(tree)
        #print(self.modules)
        return self.modules


def find_module(name, tree):
    # checks if relvant module is included
    modules = ImportVisitor().get_list(tree)
    #print(modules)
    if name in modules:
        return True
    return False



class FunctionVisitor(ast.NodeVisitor):
    # to successfully hand the information over to the comparator
    # we need to have a comparator and know the json file to read
    # the dict from
    def __init__(self, json_source):
        ast.NodeVisitor.__init__(self)
        self.comp = Comparator()
        self.json_source = json_source


    def visit_Call(self, node: ast.Call) -> Any:
        # collect relevant information about call

        # note that name contains class obj name as well if method
        name = self.get_name(node)
        line = node.lineno
        keywords = self.get_keywords(node)

        #hand information over to comparator
        self.comp.compare(name, keywords, line, self.json_source)

        #print('FUNCTION CALL of function ', name)


    def visit_Attribute(self, node: ast.Attribute):
        attrs = []
        if type(node.value) == ast.Name:
            attrs.append(node.value.id)
        if type(node.value) == ast.Attribute:
            attrs = self.visit(node.value)
        if node.attr:
            attrs.append(node.attr)
        return attrs


    def get_name(self, node):
        name = ''
        if type(node.func) == ast.Name:
            if type(node.func.id) == type(' '):
                name = node.func.id
        if type(node.func) == ast.Attribute:
                name = '.'.join(self.visit(node.func))
        return name


    @staticmethod
    def get_keywords(node):
        # get keywords of function
        # keywords are the names of named args
        list = []
        for keyword in node.keywords:
            list.append(keyword.arg)
        return list


def check_file(path, package, json_source):
    # open file to parse
    file = open(path, mode='r')
    contents = file.read()
    tree = ast.parse(contents)

    # parse only if package is imported
    if find_module(package, tree):
        print('parsing file', path)
        v = FunctionVisitor(json_source)
        v.visit(tree)
    # else do not parse
    else:
        print(path, 'does not import ', package)
        print('Therefore the file will not be analysed further.')



'''
if __name__ == '__main__':
    # main for testing
    # will be rewritten for outside calls to a function
    # returns
    #   None: no relevant modules included
    #   Dict: else

    file = open('example.py', mode ='r')
    contents = file.read()
    tree = ast.parse(contents)
    FunctionVisitor().visit(tree)


    file = open('example2.py', mode='r')
    contents = file.read()
    tree = ast.parse(contents)
    FunctionVisitor().visit(tree)



    if find_module('torch', tree):
        print('torch wurde in der Datei importiert.')
    else:
        print('torch wurde in der Datei nicht importiert.')

    #FunctionVisitor().visit(ast.parse("print('text')"))
    #FunctionVisitor().visit(ast.parse("randn(a,b)"))
'''
