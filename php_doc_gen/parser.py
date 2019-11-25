import logging
import os
import sys
from .items import *
from .docblock import Docblock
from .tag import *
from .utils import *


# We should know the State we are inside,
# GLOBAL - global scope
# IN_CLASS - inside class
# IN_INTERFACE - inside interface
# IN_TRAIT - inside trait
# OUT_OF_PHP - outside <?php  ?>
# IN_DOCBLOCK - inside docblock
# IN_FUNCTION - inside function
# IN_METHOD - inside method
class State(enum.Enum):
    GLOBAL = 1
    IN_CLASS = 2
    IN_INTERFACE = 3
    IN_TRAIT = 4
    OUT_OF_PHP = 5
    IN_DOCBLOCK = 6
    IN_FUNCTION = 7
    IN_METHOD = 8


class Parser:

    def __init__(self, filepath):

        # current state
        self.state = State.OUT_OF_PHP

        # lines of file : each element is a separate line
        self.lines = []

        # in case the file includes more than one namespace
        self.namespaces = []

        # global namespace
        self.root_namespace = Namespace('/', None, os.path.split(filepath)[1][:-4], os.path.dirname(filepath))

        # name of namespace we stand inside at the moment
        self.cur_namespace = self.root_namespace

        # name of function we stand inside at the moment
        self.cur_function = Function('')

        # name of class we stand inside at the moment
        self.cur_class = Class('', self.root_namespace)

        # name of interface we stand inside at the moment
        self.cur_interface = Interface('', self.root_namespace)

        # name of trait we stand inside at the moment
        self.cur_trait = Trait('', self.root_namespace)

        # name of method we stand inside at the moment
        self.cur_method = Method('', AccessModifier.public)

        # the difference between '{' and '}' numbers
        self.braces_diff = 0

        # whether the previous object is docblock
        self.is_prev_docblock = False

        # whether the docblock is the first-level docblock
        self.is_first_level_docblock = True

        self.cur_docblock = Docblock

        if not os.path.isfile(filepath):
            logging.info("ERROR: " + "File path {} does not exist. Exiting...".format(filepath))
            sys.exit(-1)

        with open(filepath) as fp:
            lines = fp.readlines()

            for line in lines:
                # replace multiple whitespaces with a single whitespace
                line = re.sub(' +', ' ', line)
                # remove leading and trailing whitespaces
                line = line.strip()
                # add only not empty lines
                if line:
                    self.lines.append(line)

    def parse(self):
        state = self.state
        prev_state = state  # for comment
        docblock = []
        source_block = []
        line_num = 0
        for line in self.lines:
            line_num += 1
            if state == State.OUT_OF_PHP:
                if line.find("<?php") == 0:
                    if is_namespace_line(line):
                        self.cur_namespace = self.root_namespace.add_namespace(parser_namespace(line))
                    prev_state = state
                    state = State.GLOBAL
                else:
                    logging.info('FORMAT ERROR: line should start with <?php')
                    sys.exit(-1)
            elif state == State.GLOBAL:
                if line == "?>":  # end of namespace
                    state = State.OUT_OF_PHP
                elif line == "/**":
                    prev_state = state
                    state = State.IN_DOCBLOCK
                elif is_namespace_line(line):
                    self.is_first_level_docblock = False
                    self.is_prev_docblock = False
                    self.cur_namespace = self.root_namespace.add_namespace(parser_namespace(line))
                elif is_global_var_line(line):
                    self.is_first_level_docblock = False
                    self.root_namespace.add_global_var(parser_global_var(line))
                elif is_var_line(line):
                    self.is_first_level_docblock = False
                    self.root_namespace.add_global_var(parser_var(line))
                elif is_define_line(line):
                    self.is_first_level_docblock = False
                    self.root_namespace.add_constants(parser_define(line))
                elif is_const_line(line):
                    self.is_first_level_docblock = False
                    self.root_namespace.add_constants(parser_const(line))
                elif is_function_line(line):
                    self.is_first_level_docblock = False
                    self.cur_function = parser_function(line)
                    self.cur_namespace.add_function(self.cur_function)
                    self.braces_diff = 0
                    state = State.IN_FUNCTION
                elif is_class_line(line):
                    self.is_first_level_docblock = False
                    self.cur_class = parser_class(line, self.cur_namespace)
                    self.cur_namespace.add_class(self.cur_class)
                    state = State.IN_CLASS
                elif is_interface_line(line):
                    self.is_first_level_docblock = False
                    self.cur_interface = parser_interface(line, self.cur_namespace)
                    self.cur_namespace.add_interface(self.cur_interface)
                    state = State.IN_INTERFACE
                elif is_trait_line(line):
                    self.is_first_level_docblock = False
                    self.cur_trait = parser_trait(line, self.cur_namespace)
                    self.cur_namespace.add_trait(self.cur_trait)
                    state = State.IN_TRAIT
                else:
                    logging.info('WARN: line ' + str(line_num) + ' ' + line + ' is not recognized in global state')
            elif state == State.IN_DOCBLOCK:
                if line == "*/":
                    if self.is_first_level_docblock and prev_state == State.GLOBAL and self.is_prev_docblock:
                        self.root_namespace.process_docblock(self.cur_docblock)
                        self.is_first_level_docblock = False
                    state = prev_state
                    self.cur_docblock = parser_docblock(docblock)
                    docblock = []
                    self.is_prev_docblock = True
                else:
                    docblock.append(line)
            elif state == state.IN_FUNCTION:
                if line[0] == '{':
                    self.braces_diff += 1
                elif line[0] == '}':
                    self.braces_diff -= 1
                else:
                    pass
                if self.braces_diff == 0:
                    source_block.append(line)
                    self.cur_function.set_source_body(source_block)
                    if self.is_prev_docblock:
                        self.cur_function.process_docblock(self.cur_docblock)
                    source_block = []
                    state = State.GLOBAL
                    self.is_prev_docblock = False
                else:
                    if is_global_var_line(line):
                        self.root_namespace.add_global_var(parser_global_var(line))
                    source_block.append(line)
            elif state == state.IN_CLASS:
                if line[0] == '}':
                    self.cur_class = Class('', self.cur_namespace)
                    state = state.GLOBAL
                    self.is_prev_docblock = False
                elif line == "/**":
                    prev_state = state
                    state = State.IN_DOCBLOCK
                elif is_property_var_line(line):
                    self.cur_class.add_property(parser_property_var(line))
                elif is_property_const_line(line):
                    self.cur_class.add_constant(parser_property_const(line))
                elif is_method_line(line):
                    prev_state = state
                    state = state.IN_METHOD
                    self.cur_method = parser_method(line)
                    self.cur_class.add_method(self.cur_method)
                    self.braces_diff = 0
            elif state == state.IN_INTERFACE:
                if line[0] == '}':
                    self.cur_interface = Interface('', self.cur_namespace)
                    state = state.GLOBAL
                    self.is_prev_docblock = False
                elif line == "/**":
                    prev_state = state
                    state = State.IN_DOCBLOCK
                elif is_property_const_line(line):
                    self.cur_interface.add_constant(parser_property_const(line))
                elif is_method_line(line):
                    self.cur_interface.add_method(parser_method(line))
                    self.braces_diff = 0
            elif state == state.IN_TRAIT:
                if line[0] == '}':
                    self.cur_trait = Trait('', self.cur_namespace)
                    state = state.GLOBAL
                    self.is_prev_docblock = False
                elif line == "/**":
                    prev_state = state
                    state = State.IN_DOCBLOCK
                elif is_property_var_line(line):
                    self.cur_trait.add_property(parser_property_var(line))
                elif is_method_line(line):
                    prev_state = state
                    state = state.IN_METHOD
                    self.cur_method = parser_method(line)
                    self.cur_trait.add_method(self.cur_method)
                    self.braces_diff = 0
            elif state == state.IN_METHOD:
                if line[0] == '{':
                    self.braces_diff += 1
                elif line[0] == '}':
                    self.braces_diff -= 1
                else:
                    pass
                if self.braces_diff == 0:
                    source_block.append(line)
                    self.cur_method.set_source_body(source_block)
                    source_block = []
                    state = prev_state
                    self.is_prev_docblock = False
                else:
                    source_block.append(line)
        return self.root_namespace


def parser_namespace(line):
    if line.find("<?php") != -1:
        line = line[line.find("<?php") + 6:]
    nm_name = line[line.find("namespace") + 10:]
    nm_name = nm_name[:-1]  # delete last character ';'
    nm_name.strip()
    return nm_name


def parser_docblock(docblock):

    true_docblock = []  # true_docblock is a docblock without empty lines

    # skip empty lines
    for line in docblock:
        pos = line.find('*') + 1
        nline = line[pos:]
        nline = nline.strip()
        if nline:
            true_docblock.append(nline)

    if not true_docblock:
        logging.info("BAD STYLE: no docblock summary")
        logging.info("BAD STYLE: no docblock description")
        logging.info("BAD STYLE: no docblock tag")
        return

    print("--------------")
    print("true_docblock: ")
    for line in true_docblock:
        print(line)
    print("--------------")

    # get docblock summary
    if is_tag_line(true_docblock[0]):
        logging.info("BAD STYLE: no docblock summary")
        summary = ""
    else:
        summary = true_docblock[0]
        logging.info("GOOD STYLE: docblock summary is " + summary)
        true_docblock.pop(0)  # remove summary

    # get docblock description
    description = ""
    while len(true_docblock) and not is_tag_line(true_docblock[0]):
        desc = true_docblock[0]
        description += desc
        true_docblock.pop(0)

    if not len(description):
        logging.info("BAD STYLE: no docblock description")
    else:
        logging.info("GOOD STYLE: docblock description is " + description)

    tags = []
    for line in true_docblock:
        if not is_tag_line(line):
            logging.info("BAD STYLE: should be tag line")
        else:
            tag = parser_tag(line)
            if not tag:
                logging.info("Error: can't parse the tag")
            else:
                tags.append(tag)
                logging.info("GOOD STYLE: tag parsed")

    return Docblock(summary, description, tags)


# Test function to parse docblock
def test_parser_docblock():
    # docblock - test docblock
    docblock_str = """ * The first example class, this is in the same package as the
 * procedural stuff in the start of the file
 *
 * desc
 * @package sample
 * @subpackage classes""".split('\n')

    docblock = parser_docblock(docblock_str)

    print("summary: " + docblock.get_summary())
    print("description: " + docblock.get_description())
    for tag in docblock.get_tags():
        print(tag.get_tg_name())


# required: 'str' consists of @tag info only
def parser_tag(str):
    if str.find("@author") == 0:
        author_name = ""
        author_email = ""
        pos_name = str.find('author') + 7
        pos_email = str.find('<')

        if pos_email != -1:
            author_name = str[pos_name:pos_email]
            author_email = str[pos_email + 1:str.find('>')]
        else:
            author_name = str[pos_name:]
            logging.info("BAD STYLE: no author email")

        if not len(author_name):
            logging.info("BAD STYLE: no author name")
        logging.info("GOOD STYLE: Tag_Author parsed")
        return Tag_Author(author_name, author_email)
    elif str.find("@version") == 0:
        pos_version = str.find('version') + 8
        version = str[pos_version:]
        if not len(version):
            logging.info("BAD STYLE: version missed")
            return
        logging.info("GOOD STYLE: Tag_Version parsed")
        return Tag_Version(version)
    elif str.find("@package") == 0:
        pos_package = str.find('package') + 8
        package = str[pos_package:]
        if not len(package):
            logging.info("BAD STYLE: package missed")
            return
        logging.info("GOOD STYLE: Tag_Package parsed")
        return Tag_Package(package)
    elif str.find("@var") == 0:
        type_pos = str.find("var") + 4
        str = str[type_pos:]
        if str.find(' ') != -1:
            var_name_pos = str.find(' ')
        else:
            var_name_pos = len(str)
        __type = str[:var_name_pos]
        if not len(__type):
            logging.info("BAD STYLE: var missed")
            return
        str = str[var_name_pos+1:]
        if str.find(' ') != -1:
            var_desc_pos = str.find(' ')
        else:
            var_desc_pos = len(str)
        var_name = str[:var_desc_pos]
        if not len(var_name):
            logging.info("BAD STYLE: var name missed")
            return
        desc = str[var_desc_pos+1:]
        if not len(desc):
            logging.info("BAD STYLE: no var description")
        logging.info("GOOD STYLE: Tag_Var parsed")
        return Tag_Var(var_name, __type, desc)
    elif str.find("@name") == 0:
        pos_name = str.find('name') + 5
        name = str[pos_name:]
        if not len(name):
            logging.info("BAD STYLE: name missed")
            return
        logging.info("GOOD STYLE: Tag_Name parsed")
        return Tag_Name(name)
    elif str.find("@param") == 0:
        pos_type = str.find('param') + 6
        str = str[pos_type:]
        if not len(str):
            logging.info("BAD STYLE: param missed")
            return
        pos_name = str.find(' ') + 1
        type = str[:pos_name - 1]
        if not len(type):
            logging.info("BAD STYLE: param missed")
            return
        str = str[pos_name:]
        if str.find(' ') != -1:
            pos_description = str.find(' ')
        else:
            pos_description = len(str)
        name = str[1:pos_description]
        if not len(name):
            logging.info("BAD STYLE: no param varname")
        str = str[pos_description + 1:]
        description = str
        if not len(description):
            logging.info("BAD STYLE: no param description")
        logging.info("GOOD STYLE: Tag_Param parsed")
        return Tag_Param(type, name, description)
    elif str.find("@return") == 0:
        pos_type = str.find("return") + 7
        str = str[pos_type:]
        if not len(str):
            logging.info("BAD STYLE: return missed")
            return
        if str.find(' ') != -1:
            pos_description = str.find(' ') + 1
        else:
            pos_description = len(str)
        print(pos_description)
        type = str[:pos_description]
        str = str[pos_description:]
        description = str
        if not len(description):
            logging.info("BAD STYLE: no return description")
        logging.info("GOOD STYLE: Tag_Return parsed")
        return Tag_Return(type, description)
    else:
        logging.info("ERROR: tag not found")
        return


# @param str string with var
# @param type_ var type (default empty(no type) )
# required : two required whitespaces (before and after = )
def parser_var(str, type_=""):
    # replace multiple whitespaces with a single whitespace
    str = re.sub(' +', ' ', str)
    # remove leading and trailing whitespaces
    str = str.strip()

    if str.find('=') != -1:
        var_name = str[1:str.find('=')-1]
    else:
        var_name = str[1:str.find(';')]
    print(var_name)
    return Global_var(var_name, type_)


def test_parser_var():
    # var string example
    # required : two required whitespaces (before and after = )
    var = "   $var = 'value';   "
    parser_var(var)

    # required: no whitespace between varname and ;
    var = "   $var;  "
    parser_var(var)


# @param str string with global_var
# @param type_ var type (default empty(no type) )
# required : two whitespaces (before and after = )
# required: no whitespace inside []
def parser_global_var(str, type_=""):
    # replace multiple whitespaces with a single whitespace
    str = re.sub(' +', ' ', str)
    # remove leading and trailing whitespaces
    str = str.strip()

    var__pos = str.find('[') + 2
    var_end = str.find(']') - 1
    var_name = str[var__pos:var_end]
    print(var_name)
    return Global_var(var_name, type_)


def test_parser_global_var():
    global_var = "  $GLOBALS['var'] = 1;    "
    parser_global_var(global_var)


# @param str string with define
# required: one whitespace after ,
# required: no whitespace inside ()
def parser_define(str):
    const_name = str[str.find("(") + 2:str.find(",") - 1]
    const_value = str[str.find(',') + 2:str.find(")")]
    print(const_name)
    print(const_value)
    return Global_const(const_name, const_value)


def test_parser_define():
    define = "     define('const_name', const_value);   "
    parser_define(define)


# @param str string with const
# required: one whitespace after const
# required : two whitespaces (before and after = )
def parser_const(str):
    const_name = str[str.find("const") + 6:str.find("=") - 1]
    const_value = str[str.find('=') + 2:str.find(";")]
    print(const_name)
    print(const_value)
    return Global_const(const_name, const_value)


def test_parser_const():
    const = "     const a = 1;   "
    parser_const(const)


# @param str string with function
# @param return_type type if function @return tag is specified above
# required: one whitespace between 'function' and function name
# required: no whitespace between function name and '('
def parser_function(str, return_type=""):

    function_name = str[str.find("function") + 9:str.find('(')]
    print(function_name)

    # remove function name from str
    str = str[str.find('('):]

    parameters = []

    while str.find('$') != -1:
        if str.find(',') != -1:
            pos_var_end = str.find(',')
        else:
            pos_var_end = str.find(')')

        parameters.append(Global_var(str[str.find('$')+1:pos_var_end]))
        str = str[pos_var_end + 1:]

    print('------------')
    print('parameters: ')
    for param in parameters:
        print(param)
    print('------------')

    func = Function(function_name, return_type)
    func.set_parameters(parameters)
    return func


def test_parser_function():
    function = "    function method($var1, $var2, $varn)   "
    parser_function(function)


# @param str string with class
# required: one whitespace between 'class' and class name
# required: one whitespace between class name and 'extends'/'implements'
# required: one whitespace between 'extends'/'implements' and class/interface name
def parser_class(str, namespace=None):

    extends_name = implements_name = ""
    if str.find("extends") != -1:
        class_name = str[str.find("class") + 6:str.find("extends")-1]
        extends_name = str[str.find("extends") + 8:]
    elif str.find("implements") != -1:
        class_name = str[str.find("class") + 6:str.find("implements") - 1]
        implements_name = str[str.find("implements") + 11:]
    else:
        class_name = str[str.find("class") + 6:]
    print("Class name: " + class_name)
    print("Parent class: " + extends_name)
    print("Interface: " + implements_name)
    return Class(class_name, namespace, extends_name, implements_name)


def test_parser_class():
    class_ = "    class MyClass extends MyClass2   "
    parser_class(class_)

    class_ = "    class MyClass   "
    parser_class(class_)

    class_ = "    class MyClass implements MyClass2_interface   "
    parser_class(class_)


# @param str string with interface
# required: one whitespace between 'interface' and class name
# required: one whitespace between interface name and 'extends''
# required: one whitespace between 'extends' and interface name
# required: one whitespace between comma and interface name
def parser_interface(str, namespace=None):

    parents = []

    if str.find("extends") != -1:
        interface_name = str[str.find("interface") + 10:str.find("extends")-1]
        parents_names = str[str.find("extends") + 8:]
        parents = parents_names.split(', ')
        for i in parents:
            print(i)
    else:
        interface_name = str[str.find("interface") + 10:]

    print("Interface: " + interface_name)
    return Interface(interface_name, namespace, parents)


def test_parser_interface():
    interface = "   interface a   "
    parser_interface(interface)

    interface = "   interface a extends b  "
    parser_interface(interface)

    interface = "   interface a extends b, c, d  "
    parser_interface(interface)


# @param str string with trait
# required: one whitespace between 'trait' and trait name
def parser_trait(str, namespace=None):

    trait_name = str[str.find("trait") + 6:]
    print("Trait name: " + trait_name)
    return Trait(trait_name, namespace)


def test_parser_trait():
    trait = "   trait a   "
    parser_trait(trait)


def parser_property_var(str):

    # remove static keyword if exists
    if re.match(r'static ', str):
        str = str[7:]
    elif re.match(r'.* static .*', str):
        str = str.replace(' static ', ' ')

    if str[0] == '$' or str.find('public') != -1:
        if str.find('=') != -1:
            var_name = str[str.find('$')+1:str.find('=') - 1]
        else:
            var_name = str[str.find('$')+1:str.find(';')]
        print('public ' + var_name)
        return Property(var_name, AccessModifier.public)
    elif str.find('protected') != -1:
        if str.find('=') != -1:
            var_name = str[str.find('$')+1:str.find('=') - 1]
        else:
            var_name = str[str.find('$')+1:str.find(';')]
        print('protected ' + var_name)
        return Property(var_name, AccessModifier.protected)
    elif str.find('private') != -1:
        if str.find('=') != -1:
            var_name = str[str.find('$')+1:str.find('=') - 1]
        else:
            var_name = str[str.find('$')+1:str.find(';')]
        print('private ' + var_name)
        return Property(var_name, AccessModifier.private)
    else:
        logging.info("BAD STYLE: property_var not found")


def test_parser_property_var():

    var = "$var = 1;"  # it's public
    parser_property_var(var)

    var = "public $var;"
    parser_property_var(var)

    var = "protected $var = 'string';"
    parser_property_var(var)

    var = "private $var = 1.54;"
    parser_property_var(var)

    var = "public static $var;"  # just ignore static
    parser_property_var(var)

    var = "static $var;"  # just ignore static, it's public
    parser_property_var(var)


def parser_property_const(str):

    if re.match('const ', str) or re.match('public ', str):
        const_name = str[str.find('const')+6:str.find('=') - 1]
        const_val = str[str.find('=')+2:str.find(';')]
        print('public ' + const_name + ' = ' + const_val)
        return Const(const_name, AccessModifier.public, const_val)
    elif re.match('protected ', str):
        const_name = str[str.find('const')+6:str.find('=') - 1]
        const_val = str[str.find('=') + 2:str.find(';')]
        print('protected ' + const_name + ' = ' + const_val)
        return Const(const_name, AccessModifier.protected, const_val)
    elif re.match('private ', str):
        const_name = str[str.find('const')+6:str.find('=') - 1]
        const_val = str[str.find('=') + 2:str.find(';')]
        print('private ' + const_name + ' = ' + const_val)
        return Const(const_name, AccessModifier.private, const_val)
    else:
        logging.info("BAD STYLE: property_const not found")
        raise Exception("it's not a property_const line")


def test_parser_property_const():

    const = "const a = 1;"  # it's public

    const = "public const a = 'string';  "

    const = "protected const a = 1.33;"

    const = "private const a = 'blabla';"

    const = "protected static const b = 1;"


def parser_method(str, return_type=""):

    am = AccessModifier.public

    if re.match('public ', str):
        str = str[7:]
    elif re.match('protected ', str):
        am = AccessModifier.protected
        str = str[10:]
    elif re.match('private ', str):
        am = AccessModifier.private
        str = str[8:]

    method_name = str[str.find("function") + 9:str.find('(')]
    print(method_name)

    # remove function name from str
    str = str[str.find('('):]

    parameters = []

    while str.find('$') != -1:
        if str.find(',') != -1:
            pos_var_end = str.find(',')
        else:
            pos_var_end = str.find(')')

        parameters.append(Global_var(str[str.find('$') + 1:pos_var_end]))
        str = str[pos_var_end + 1:]

    print('------------')
    print('parameters: ')
    for param in parameters:
        print(param.get_name())
    print('------------')

    meth = Method(method_name, am, return_type)
    print("method_name = " + method_name + ", AccessModifier = " + am.name + ", return_type = " + return_type)
    meth.set_parameters(parameters)
    return meth


def test_parser_method():

    method = "  function method($var1)"  # it's public
    parser_method(method)

    method = "  public function method()"
    parser_method(method)

    method = "  protected function method($var1, $var2, $var3)"
    parser_method(method)

    method = " private function method($var2, $var1)"
    parser_method(method)

    method = "private static function method($var)"
    parser_method(method)


def main():
    with open('php_doc_gen.log', 'w') as f:
        pass
    logging.basicConfig(filename='php_doc_gen.log', level=logging.INFO)
    ps = Parser(r'D:\recFolder\f2.php')

    nm = ps.parse()
    pass


if __name__ == '__main__':
    main()
