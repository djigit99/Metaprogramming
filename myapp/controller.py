from myapp.parser import Parser
from myapp.generator import *
from myapp.azindex import Content

from os import listdir
from os.path import isfile, isdir, join, splitext, dirname


def doc_file(path, output_path, content):
    p = Parser(path)
    nm = p.parse()
    content.process_namespace(nm)
    gen_preload(dirname(path), output_path)
    gen_sidebar(dirname(path), output_path, False, True, nm.get_filename())
    gen_file(nm, dirname(path), output_path, content)
    gen_namespace_hierarchy(nm, output_path, content)


def doc_folder(path, output_path, content):
    php_files = [f for f in listdir(path) if isfile(join(path, f)) and splitext(f)[1] == '.php']
    gen_preload(path, output_path)
    read_me = []
    if isfile(os.path.join(path, 'README.md')):
        with open(os.path.join(path, 'README.md'), 'r') as h_file:
            read_me = h_file.readlines()
            h_file.close()
    else:
        read_me.append('<h1><em>No documentation for this directory</em></h1>')
    gen_folder(read_me, output_path, content)
    for php_file in php_files:
        p = Parser(join(path, php_file))
        nm = p.parse()
        content.process_namespace(nm)
        gen_file(nm, path, output_path, content)
        gen_namespace_hierarchy(nm, output_path, content)


def doc_rec_folder(path, output_path, content):
    doc_folder(path, output_path, content)
    gen_sidebar(path, output_path)

    folders = [f for f in listdir(path) if isdir(join(path, f)) and f != 'docs']
    for folder in folders:
        doc_rec_folder(join(path, folder), join(output_path, folder), content)


def doc_is_rec_folder(path, output_path, content, is_rec=True):
    if not is_rec:
        doc_folder(path, output_path, content)
        gen_sidebar(path, output_path, False)
    else:
        doc_rec_folder(path, output_path, content)


class Controller:

    def __init__(self, path, output_path, is_folder=False, is_rec_search=False):
        self.content = Content(output_path)

        gen_main_page(output_path)
        if not is_folder:
            doc_file(path, output_path, self.content)
        else:
            doc_is_rec_folder(path, output_path, self.content, is_rec_search)
        gen_content(self.content, output_path)


def main():
    Controller(r'D:\recFolder', r'D:\recFolder_doc2', True, True)


if __name__ == '__main__':
    main()
