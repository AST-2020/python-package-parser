"""
Imports class stores all used imports. in named imports later called by a name prefix are stored,
and in unknown imports without a prefix needed are stored
"""


class Imports:

    def __init__(self):
        self.named = {}
        self.unknown = {}

    # add a import with alias/ asname and the package path to named
    def add_named_import(self, package, asname):
        self.named[asname] = package

    # add a import without alias/ asname and the package path to unknown
    def add_unnamed_import(self, package):
        self.unknown[package] = []

    # fill valid contents to unknown for a package
    def set_package_content(self, package, contents):
        self.unknown[package] = contents

    def get_package_from_asname(self, asname):
        return self.named[asname]

    # get package for a content item without prefix from unknown
    def get_package_from_content(self, caller):
        for package in self.unknown:
            for content in self.unknown[package]:
                if caller == content:
                    return package
        return None
