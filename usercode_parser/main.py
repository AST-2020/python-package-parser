import parser
import sys

if __name__=='__main__':

    if len(sys.argv) == 3:
        file_path = sys.argv[1]
        bib = sys.argv[2]
        if bib == 'pytorch':
            parser.check_file(file_path, 'torch', 'resultsPytorch.json')

        elif bib == 'scikit':
            parser.check_file(file_path, 'sklearn', 'resultsSciKit.json')

        else:
            print('your libray is not supported. choose between pytorch and scikit')

    else:
        print('programm expects two arguments. firstly the destination path and secondly the library to check for.')
