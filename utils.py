import re

# Check if current line has a tag
def is_tag_line(line):
    # replace multiple whitespaces with a single whitespace
    line = re.sub(' +', ' ', line)
    # remove leading and trailing whitespaces
    line = line.strip()

    line = line[line.find('*') + 2]
    return line[0] == '@'
