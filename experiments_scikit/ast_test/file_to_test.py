
from TestDirectory import file1
# Result:
# import the whole file
# parameters in Method  {'testFile1': {'__init__': ['self', 'name']}}
# parameters in Function  {'testFunc1': ['num']}

from TestDirectory.file1 import testFile1
# Result:
# only imported the class
# parameters in Method  {'__init__': ['self', 'name']}


from TestDirectory.file1 import testFunc1
# Result:
# only imported the function
# parameters in Function  ['num']

from TestDirectory import *
# Result:
# imported using __all__
# parameters in function  {'testFunc1': ['num']}

from TestDirectory import PackageInside
# Result:
# imported using __all__
# parameters in Method  {'testClass3': {'__init__': ['self']}}
# parameters in function  {'testFunc3': ['num']}


# Representation der Testdatei in Json
#
# {
#    "function": {
#       "TestDirectory.PackageInside.file3": {
#          "testFunc3": [
#             "num"
#          ]
#       },
#       "TestDirectory.file1": {
#          "testFunc1": [
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
#       "TestDirectory.file1": {
#          "testFile1": {
#             "__init__": [
#                "self",
#                "name"
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
#          [
#             "file1",
#             "testFunc1"
#          ]
#       ],
#       "TestDirectory.PackageInside": [
#          [
#             "",
#             "file3"
#          ]
#       ]
#    }
# }
