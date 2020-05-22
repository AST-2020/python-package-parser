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

    def visit_Call(self, node: ast.Call) -> Any:
        # collect relevant information about call

        # note that name contains class obj name as well if method
        prefix, name = self.get_name(node)
        line = node.lineno
        path, sub, type = self.expand_prefix(prefix, line, name)
        keywords = self.get_keywords(node)

        # hand information over to comparator
        if (type is 'function') or (type is 'method'):
            print(line, name, path, sub, type, keywords)
        # Comparator().compare(self.package_dict, path, name, keywords, line, sub, type)

    def visit_Attribute(self, node: ast.Attribute):
        attrs = []
        if type(node.value) is ast.Name:
            attrs.append(node.value.id)
        if type(node.value) is ast.Attribute:
            attrs = self.visit(node.value)
        if node.attr:
            attrs.append(node.attr)
        return attrs

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
                if prefix in module:
                    if fkt in self.package_dict['function'][module]:
                        return module
        if type == 'method':
            for module in self.package_dict['method']:
                # print(self.package_dict['method'][module])
                if cls in self.package_dict['method'][module]:
                    # if fkt in self.package_dict['method'][module][cls]:
                    return module
        return ''

    def expand_prefix(self, prefix, line, name):
        path = ''
        type = ''
        if prefix is not None:
            # if function
            if prefix in self.imports.named:
                path = self.imports.named[prefix]
                path = self.get_path(path, name, 'function')
                return path, '', 'function'

            # if method
            cls = self.vars.get_var_type(prefix, line)
            if cls is not None:
                list = cls.split('.')
                # if Constructor with alias up front
                if len(list) == 2:
                    path = self.imports.get_package_from_asname(list[0])
                    cls = list[-1]
                    if path is not None:
                        path = self.get_path(path, name, 'method', cls)
                        return path, cls, 'method'
                # if Constructor only
                else:
                    # search for path
                    path = self.imports.get_package_from_content(cls)
                    if path is not None:
                        cls = list[-1]
                        path = self.get_path(path, name, 'method', cls)
                        return path, cls, 'method'

        return path, '', type

    @staticmethod
    def get_keywords(node):
        # get keywords of function
        # keywords are the names of named args
        list = []
        for keyword in node.keywords:
            list.append(keyword.arg)
        return list