import re


def is_docblock_line(line):
    return re.match('/\*\*', line)


def is_end_docblock_line(line):
    return re.search('\*/', line)


# Check if current line has a tag
def is_tag_line(line):
    possible_tags = ['@author', '@version', '@package', '@name', '@var', '@param', '@return']
    is_tag = False
    if re.match('@[a-z]+', line):
        match = re.search('@[a-z]+', line)
        if match is not None:
            tag_name = match.group(0)
            if tag_name in possible_tags:
                if re.match('@[a-z]+', line):
                    return True
    return False


def is_namespace_line(line):
    return re.match('(<\?php\s)?namespace\s([a-zA-Z]+[\\\\]?)+', line)


def is_var_line(line):
    return re.match('[$][a-zA-Z_][\w]*', line)


def is_global_var_line(line):
    return re.match('[$]GLOBALS\[\'[a-zA-Z_][\w]*\'\]', line)


def is_define_line(line):
    return re.match('define\(.*\)', line)


def is_const_line(line):
    return re.match('const\s[a-zA-Z_][\w]*', line)


def is_function_line(line):
    return re.match('function\s[a-zA-Z_][\w]*\(.*\)', line)


def is_class_line(line):
    return re.match('(abstract\s)?class\s[a-zA-Z_][\w]*', line)


def is_interface_line(line):
    return re.match('interface\s[a-zA-Z_][\w]*', line)


def is_trait_line(line):
    return re.match('trait\s[a-zA-Z_][\w]*', line)


def is_property_var_line(line):
    return re.match('((public\s)|(protected\s)|(private\s))?(static\s)?[$][a-zA-Z_][\w]*', line)


def is_property_const_line(line):
    return re.match('((public\s)|(protected\s)|(private\s))?const\s[a-zA-Z_][\w]*', line)


def is_method_line(line):
    return re.match('(abstract\s)?((public\s)|(protected\s)|(private\s))?(static\s)?function\s[a-zA-Z_][\w]*\(.*\)', line)