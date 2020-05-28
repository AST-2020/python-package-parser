"""
this visitor scans for function and method calls. functions and methods, which can be assigned to the module
will be further analysed to gather informations about its position in the module, name, line, arguments.
These informations are then used to call a comparator method to evaluate its correctness.
"""

import ast
from typing import Any

from variables import UsedVariables
from imports import Imports
# from comparator import Comparator


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, dict, imports: Imports = Imports(), variables: UsedVariables = UsedVariables()):
        ast.NodeVisitor.__init__(self)
        self.imports: Imports = imports
        self.vars: UsedVariables = variables
        self.package_dict = dict
        # self.comp = Comparator()

    # collect relevant information about call of function or method
    def visit_Call(self, node: ast.Call) -> Any:
        # note that name contains class obj name as well if method
        prefix, name = self.get_name(node)
        line = node.lineno
        path, sub, type = self.expand_prefix(prefix, line, name)
        keywords = self.get_keywords(node)

        # hand information over to comparator
        if (type is 'function') or (type is 'method'):
            print(line, name, path, sub, type, keywords)
            # self.comp.compare(self.package_dict, path, name, keywords, line, sub, type)

    def visit_Attribute(self, node: ast.Attribute):
        attrs = []
        if type(node.value) is ast.Name:
            attrs.append(node.value.id)
        if type(node.value) is ast.Attribute:
            attrs = self.visit(node.value)
        if node.attr:
            attrs.append(node.attr)
        return attrs

    # get the function name and prefix
    def get_name(self, node):
        name = ''
        prefix = ''
        if type(node.func) == ast.Name:
            if isinstance(node.func.id, str):
                name = node.func.id
                return prefix, name
        if type(node.func) == ast.Attribute:
            list = self.visit(node.func)
            if len(list) > 1:
                prefix = '.'.join(list[:-1])
                name = list[-1]
                return prefix, name
            else:
                name = list[0]
                return prefix, name
        return prefix, name

    def get_path(self, prefix, fkt, type, cls=''):
        if type == 'function':
            for module in self.package_dict['function']:
                # if prefix is partial path
                if prefix in module:
                    if fkt in self.package_dict['function'][module]:
                        return module

            # if prefix contains whole path till function
            list = prefix.split('.')
            for i in range(len(list)-1):
                pre = '.'.join(list[:(-i)])
                if pre in self.package_dict['function'].keys():
                    return pre

        if type == 'method':
            for module in self.package_dict['method']:
                if cls in self.package_dict['method'][module]:
                    return module
        return ''

    # further expand the functions prefix, to get path in package, and wheter it's a function or method
    # returns path: the path inside the package, cls: class name if its a method, name: the function name
    def expand_prefix(self, prefix, line, name):
        path = ''
        type = ''
        if prefix is not None:
            # if function with prefix
            if prefix in self.imports.named:
                path = self.imports.get_package_from_asname(prefix, line)
                path = self.get_path(path, name, 'function')
                if path != '':
                    return path, '', 'function'

            # if Constructor with prefix
            if prefix in self.imports.named:
                path = self.imports.get_package_from_asname(prefix, line)
                path = self.get_path(path, '__init__', 'method', name)
                if path != '':
                    return path, name, 'method'

            # if method with class object as prefix
            cls = self.vars.get_var_type(prefix, line)
            if cls is not None:
                list = cls.split('.')
                # if object created with Constructor with alias up front
                if len(list) == 2:
                    path = self.imports.get_package_from_asname(list[0], line)
                    cls = list[-1]
                    if path is not None:
                        path = self.get_path(path, name, 'method', cls)
                        return path, cls, 'method'
                # if object created without alias in front of Constructor
                else:
                    # search for path
                    path = self.imports.get_package_from_content(cls, line)
                    if path is not None:
                        cls = list[-1]
                        path = self.get_path(path, name, 'method', cls)
                        return path, cls, 'method'

        if name != '':
            # if Constructor without prefix
            path = self.get_path('', name, 'method', name)
            if path is not None:
                return path, name, 'method'

        return '', '', type

    @staticmethod
    # get keywords of function, keywords are the names of named args
    def get_keywords(node):
        list = []
        for keyword in node.keywords:
            list.append(keyword.arg)
        return list
