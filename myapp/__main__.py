from .controller import Controller
from .generator import *
from .parser import Parser

ct = Controller(r'D:\recFolder', True)

gen_sidebar(r'D:\recFolder')
gen_main_page(r'D:\recFolder')


par = Parser(r'D:\recfolder\f3.php')
nm = par.parse()
#gen_file(nm.get_child_namespaces()[0].get_child_namespaces()[0], 'output_path')
#gen_class(nm.get_classes()[0])

#gen_hierarchy('D:\recfolder')
gen_namespace_hierarchy(nm)