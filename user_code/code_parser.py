"""
this visitor scans for function and method calls. functions and methods, which can be assigned to the module
will be further analysed to gather informations about its position in the module, name, line, arguments.
These informations are then used to call a comparator method to evaluate its correctness.
"""

import ast
from typing import Any

from user_code.variables import UsedVariables
from user_code.imports import Imports
from comparator.comparator import Comparator


class FunctionVisitor(ast.NodeVisitor):
    def __init__(self, file, dict, imports, variables: UsedVariables = UsedVariables()):
        ast.NodeVisitor.__init__(self)
        self.imports: Imports = imports
        self.vars: UsedVariables = variables
        self.package_dict = dict
        self.comp = Comparator(self.package_dict)
        self.file = file

    # collect relevant information about call of function or method
    def visit_Call(self, node: ast.Call) -> Any:
        # note that name contains class obj name as well if method
        prefix, name = self.get_name(node)
        line = node.lineno
        keywords = self.get_keywords(node)
        args = self.get_args(node)
        cls, package = self.get_package(prefix, name, line)
        if cls == '':
            cls = None
        if (package is not None) and (package != ""):
            # compare names of named args
            self.comp.compare_arg_names(self.file, line, package, keywords, name, cls)
            # compare arg count
            self.comp.compare_arg_amount(self.file, line, package, name, keywords, args, cls)
        """
        # if function
        package = self.imports.get_package_from_asname(prefix, line)
        if package is not None:
            if name in package.split('.'):
                package = '.'.join(package.split('.')[:-1])
            if package in self.package_dict['function']:
                self.comp.compare(self.package_dict, package, name, keywords, line)

        # if method
        cls = self.vars.get_var_type(prefix, line)
        if cls is not None:
            package = self.imports.get_package_from_asname(cls, line)
            if name in package.split('.'):
                package = '.'.join(package.split('.')[:-1])
            if cls in package.split('.'):
                package = '.'.join(package.split('.')[:-1])
            if (package is not None) and (package in self.package_dict['method']):
                self.comp.compare(self.package_dict, package, name, keywords, line, cls)
        
        # path, sub, type = self.expand_prefix(prefix, line, name)
        keywords = self.get_keywords(node)

        # hand information over to comparator
        if (type is 'function') or (type is 'method'):
            # print(line, name, path, sub, type, keywords)
            if sub is not None:
                print(sub, name, (name in self.package_dict[type][path][sub])) #':', self.package_dict[type][path][sub])
            else:
                print(name, ':', self.package_dict[type][path][name])
            # self.comp.compare(self.package_dict, path, name, keywords, line, sub)
        """

    # find the package and class if method, the function is defined at
    def get_package(self, prefix, name, line):
        if prefix is None:
            if self.imports.get_package_from_asname(name, line) is not None:
                return '', self.get_function_package('', name, line)

        else:
            if self.imports.get_package_from_asname(prefix, line) is not None:
                return '', self.get_function_package(prefix, name, line)
            cls = self.vars.get_var_type(prefix, line)
            if cls is not None:
                return cls, self.get_method_package(cls, name, line)
        return '', ''

    def get_function_package(self, prefix, name, line):
        if prefix == '':
            package = self.imports.get_package_from_asname(name, line).split('.')
            if name == package[-1]:
                package = package[:-1]
            package = '.'.join(package)
            return package
        else:
            return self.imports.get_package_from_asname(prefix, line)

    def get_method_package(self, cls, name, line):
        if cls != '':
            cls = cls.split('.')
            package = self.imports.get_package_from_asname(cls[0], line).split('.')
            cls = '.'.join(cls)
            if cls == package[-1]:
                package = package[:-1]
            package = '.'.join(package)
            return package
        return ''

    # helper function for get_name to get the full name with all prefixes
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
        name = None
        prefix = None
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

    """
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
        return None

    # further expand the functions prefix, to get path in package, and wheter it's a function or method
    # returns path: the path inside the package, cls: class name if its a method, name: the function name
    def expand_prefix(self, prefix, line, name):
        path = None
        type = None
        if prefix is not None:
            # if function with prefix
            if prefix in self.imports.named:
                path = self.imports.get_package_from_asname(prefix, line)
                path = self.get_path(path, name, 'function')
                if path is not None:
                    return path, None, 'function'

            # if Constructor with prefix
            if prefix in self.imports.named:
                path = self.imports.get_package_from_asname(prefix, line)
                path = self.get_path(path, '__init__', 'method', name)
                if path is not None:
                    return path, name, 'method'

            # if method with class object as prefix
            cls = self.vars.get_var_type(prefix, line)
            if cls is not None:
                list = cls.split('.')
                # if class type contains prefix
                if len(list) == 2:
                    path = self.imports.get_package_from_asname(list[0], line)
                    cls = list[-1]
                    if path is not None:
                        path = self.get_path(path, name, 'method', cls)
                        return path, cls, 'method'
                # if class type contains no prefix
                else:
                    # search for path
                    path = self.imports.get_package_from_content(cls, line)
                    if path is not None:
                        path = self.get_path(path, name, 'method', cls)
                        return path, cls, 'method'

        if name is not None:
            # if Constructor without prefix
            path = self.get_path(prefix, name, 'method', name)
            if path is not None:
                return path, name, 'method'

        return None, None, type
    """

    @staticmethod
    # get keywords/ named argument names of the function
    def get_keywords(node):
        list = []
        for keyword in node.keywords:
            list.append(keyword.arg)
        return list

    @ staticmethod
    # get unnamed arguments of the function
    def get_args(node):
        # print(ast.dump(node))
        args = []
        raw_args = node.args
        for arg in raw_args:
            if type(arg) == ast.Str:
                args.append(arg.s)
            else:
                args.append(arg.id)
        return args
