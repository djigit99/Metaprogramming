import enum
import logging
import os
import sys
import items
from docblock import Docblock
from tag import *

# We should know which State we are inside,
# GLOBAL - global scope
# IN_CLASS - inside class
# IN_INTERFACE - inside interface
# IN_TRAIT - inside trait
# OUT_OF_PHP - outside <?php  ?>
# IN_DOCBLOCK - inside docblock
class State(enum.Enum):
    GLOBAL = 1
    IN_CLASS = 2
    IN_INTERFACE = 3
    IN_TRAIT = 4
    OUT_OF_PHP = 5
    IN_DOCBLOCK = 6


class Parser():

    def __init__(self, filepath):

        # current state
        self.state = State.OUT_OF_PHP

        # lines of file : each element is a separate line
        self.lines = []

        # in case the file includes more than one namespace
        self.namespaces = []

        # name of namespace we stand inside at the moment
        self.cur_namespace = '/'

        if not os.path.isfile(filepath):
            logging.info("ERROR: " + "File path {} does not exist. Exiting...".format(filepath))
            sys.exit(-1)

        with open(filepath) as fp:
            line = fp.readline()
            print(line)

            # add only not empty lines
            if line:
                self.lines.append(line)

    def todo(self):
        state = self.state
        prev_state = state  # for comment
        docblock = []
        for line in self.lines:
            if state == State.OUT_OF_PHP:
                if line.find("<?php") == 0:
                    nm = parse_namespace(line)
                    self.cur_namespace = items.Namespace(nm)
                    self.namespaces.append(self.cur_namespace)
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
            elif state == State.IN_DOCBLOCK:
                if line == "*/":
                    state = prev_state
                    parse_docblock(docblock)
                    docblock.clear()
                else:
                    docblock.append(line)


def parse_namespace(line):
    str = line[line.find("<?php") + 6:]
    if str.find("namespace") != -1:
        nm_name = str[str.find("namespace") + 10:]
        nm_name = nm_name[:-1]  # delete last character ';'
    else:
        nm_name = "/"
    return nm_name


def parse_docblock(docblock):
    if not docblock:
        logging.info("BAD STYLE: no docblock summary")
        logging.info("BAD STYLE: no docblock description")
        logging.info("BAD STYLE: no docblock tag")
        return

    true_docblock = []  # true_docblock is a docblock without empty lines

    # skip empty lines
    for line in docblock:
        pos = line.find('*') + 1
        if line[pos:]:
            true_docblock.append(line)

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
        summary = summary[summary.find('*') + 2:]
        logging.info("GOOD STYLE: docblock summary is " + summary)
        true_docblock.pop(0)  # remove summary

    # get docblock description
    description = ""
    while len(true_docblock) and not is_tag_line(true_docblock[0]):
        desc = true_docblock[0]
        desc = desc[desc.find('*') + 2:]
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
            line = line[line.find('*') + 2:]
            tag = parser_tag(line)
            if not tag:
                logging.info("Error: can't parse the tag")
            else:
                tags.append(tag)
                logging.info("GOOD STYLE: tag parsed")

    return Docblock(summary, description, tags)


# Test function to parse docblock
def test_parse_docblock():
    # docblock - test docblock
    docblock_str = """ * The first example class, this is in the same package as the
 * procedural stuff in the start of the file
 *
 * desc
 * @package sample
 * @subpackage classes""".split('\n')

    docblock = parse_docblock(docblock_str)

    print("summary: " + docblock.get_summary())
    print("description: " + docblock.get_description())
    for tag in docblock.get_tags():
        print(tag.get_tg_name())


# Check if current line has a tag
def is_tag_line(line):
    line = line[line.find('*') + 2]
    return line[0] == '@'


# Consider that the 'str' consists of @tag info only
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
    elif str.find("@global") == 0:
        type_pos = str.find("global") + 7
        str = str[type_pos:]
        if str.find(' ') != -1:
            info_pos = str.find(' ')
        else:
            info_pos = len(str)
        __type = str[:info_pos]
        if not len(__type):
            logging.info("BAD STYLE: global missed")
            return
        info = str[info_pos:]
        if not len(info):
            logging.info("BAD STYLE: no global information")
        logging.info("GOOD STYLE: Tag_Global parsed")
        return Tag_Global(__type, info)
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
        name = str[:pos_description]
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


def parser_define(str):
    str = str[str.find("define") + 8:]  # 8 is length of " define(' "
    var_name = str[:str.find("'")]
    str = str[str.find("'") + 2:]
    var_value = str[:str.find(')')]
    print(var_value)


def parser_class(str):
    first_row = str[0]
    class_name = first_row[first_row.find("class") + 6:]
    print(class_name)


def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    test_parse_docblock()


if __name__ == '__main__':
    main()
