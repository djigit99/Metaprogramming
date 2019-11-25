from myapp.parser import Parser
from myapp.generator import *

from os import listdir, walk
from os.path import isfile, isdir, join, splitext, dirname


def doc_file(path, output_path):
    p = Parser(path)
    nm = p.parse()
    gen_preload(dirname(path), output_path)
    gen_sidebar(dirname(path), output_path, False, True, nm.get_filename())
    gen_file(nm, dirname(path), output_path)
    gen_namespace_hierarchy(nm, output_path)


def doc_folder(path, output_path):
    php_files = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1] == '.php']
    gen_preload(path, output_path)
    for php_file in php_files:
        p = Parser(join(path, php_file))
        nm = p.parse()
        gen_file(nm, path, output_path)
        gen_namespace_hierarchy(nm, output_path)


def doc_rec_folder(path, output_path):
    doc_folder(path, output_path)
    gen_sidebar(path, output_path)

    folders = [f for f in listdir(path) if isdir(join(path, f)) and f != 'docs']
    for folder in folders:
        doc_rec_folder(join(path, folder), join(output_path, folder))


def doc_is_rec_folder(path, output_path, is_rec=True):
    if not is_rec:
        doc_folder(path, output_path)
        gen_sidebar(path, output_path, False)
    else:
        doc_rec_folder(path, output_path)


class Controller:

    def __init__(self, path, output_path, is_folder=False, is_rec_search=False):
        gen_main_page(output_path)
        if not is_folder:
            doc_file(path, output_path)
        else:
            doc_is_rec_folder(path, output_path, is_rec_search)


def main():
    Controller(r'D:\recFolder', r'D:\recFolder_doc2', True, True)


if __name__ == '__main__':
    main()
