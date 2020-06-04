# A class to save and access imports from the user code


class Imports:

    def __init__(self):
        self.named = {}
        self.unknown = {}

    def add_named_import(self, package, asname):
        self.named[asname] = package

    def add_unnamed_import(self, package):
        self.unknown[package] = []

    def set_package_content(self, package, contents):
        self.unknown[package] = contents

    def get_package_from_asname(self, asname):
        return self.named[asname]

    def get_package_from_content(self, caller):
        for package in self.unknown:
            for content in self.unknown[package]:
                if caller == content:
                    return package
        return None
