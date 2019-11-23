from .parser import Parser

from os import listdir, walk
from os.path import isfile, join, splitext


class Controller:

    def __init__(self, path, is_folder=False, is_rec_search=False):
        if not is_folder:
            p = Parser(path)
            #nm = p.parse()
            pass
        elif not is_rec_search:
            php_files = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1]=='.php']
            for php_file in php_files:
                print(php_file)


ctrl = Controller(r'D:\recFolder')

