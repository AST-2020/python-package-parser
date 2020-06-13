class Imports:
    """
    Imports class stores all used imports. in named imports later called by a name prefix are stored,
    and in unknown imports without a prefix needed are stored
    """

    def __init__(self):
        self.named = {}
        self.unknown = {}

    # add a import with alias/ asname and the package path to named
    def add_named_import(self, package, line, asname):
        self.named[asname] = (package, line)

    # add a import without alias/ asname and the package path to unknown
    def add_unnamed_import(self, package, line):
        self.unknown[package] = ([], line)

    # fill valid contents to unknown for a package
    def set_package_content(self, package, contents):
        self.unknown[package] = (contents, self.unknown[package][1])

    def get_package_from_asname(self, asname, line):
        if asname in self.named:
            if line >= self.named[asname][1]:
                return self.named[asname][0]
        else:
            return None

    """
    # get package for a content item without prefix from unknown
    def get_package_from_content(self, caller, line):
        for package in self.unknown:
            if line >= self.unknown[package][1]:
                for content in self.unknown[package][0]:
                    if caller == content:
                        return package
        return None
    """
