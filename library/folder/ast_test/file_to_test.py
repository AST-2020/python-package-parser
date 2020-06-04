# from TestDirectory import file1, file2
# Result:
# import the whole file
# parameters in Method  {'testFile1': {'__init__': ['self', 'name']}}
# parameters in Function  {'testFunc1': ['num']}

# import TestDirectory.file1
# Result:
# import the whole file
# parameters in Method  {'testFile1': {'__init__': ['self', 'name']}}
# parameters in Function  {'testFunc1': ['num']}


# from TestDirectory.file1 import testFile1
# Result:
# only imported the class
# parameters in Method  {'__init__': ['self', 'name']}

# from TestDirectory.file1 import testFunc1
# Result:
# only imported the function
# parameters in Function  ['num']

from TestDirectory import *
# Result:
# imported using __all__
# parameters in function  {'testFunc1': ['num']}

# from TestDirectory import PackageInside
# Result:
# imported using __all__
# parameters in Method  {'testClass3': {'__init__': ['self']}}
# parameters in function  {'testFunc3': ['num']}

# import TestDirectory.file1

# Representation der Testdatei in Json
#
# {
#    "function": {
#       "TestDirectory.PackageInside.file3": {
#          "testFunc3": [
#             "num"
#          ]
#       },
#       "TestDirectory.__init__": {
#          "func_in_init": [
#             "init_args",
#             "cool"
#          ],
#          "func_in_init_2": [
#             "not_cool"
#          ]
#       },
#       "TestDirectory.file1": {
#          "testFunc1": [
#             "num"
#          ],
#          "testFunc2": [
#             "num"
#          ]
#       },
#       "TestDirectory.file2": {
#          "testFunc2": [
#             "num"
#          ]
#       }
#    },
#    "method": {
#       "TestDirectory.PackageInside.file3": {
#          "testClass3": {
#             "__init__": [
#                "self"
#             ],
#             "methode3": [
#                "self",
#                "args"
#             ]
#          }
#       },
#       "TestDirectory.PackageInside.file4": {
#          "testFile4": {
#             "__init__": [
#                "self",
#                "name"
#             ]
#          }
#       },
#       "TestDirectory.__init__": {
#          "cls_in_init": {
#             "__init__": [
#                "self"
#             ],
#             "method_in_init": [
#                "self",
#                "really_cool"
#             ]
#          }
#       },
#       "TestDirectory.file1": {
#          "testFile1": {
#             "__init__": [
#                "self",
#                "name"
#             ]
#          },
#          "testFile2": {
#             "__init__": [
#                "self",
#                "name2"
#             ]
#          }
#       },
#       "TestDirectory.file2": {
#          "testFile2": {
#             "__init__": [
#                "self",
#                "name"
#             ]
#          }
#       }
#    },
#    "package__all__list": {
#       "TestDirectory": [
#          "file1.testFunc1",
#          "file1.testFile1",
#          "func_in_init",
#          "cls_in_init",
#          "PackageInside.file3",
#          "PackageInside"
#       ],
#       "TestDirectory.PackageInside": [
#          "file3"
#       ]
#    }
# }
