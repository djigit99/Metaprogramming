import os
from bs4 import BeautifulSoup

# Find depth of path
def path_depth(path):
    return path.count('\\') + 1

# Generate html docs
def __gen__(path):
    tree = os.walk(path)
    html_code = '<!DOCTYPE html><html>'
    html_code += """ <head>
    <meta charset="UTF-8">
    <link href="css/treeViewSheet.css" rel="stylesheet" media="all"/>
    <link href="css/navbar-fixed-left.css" rel="stylesheet" media="all"/>
    <title>Title</title>
    </head>"""
    html_code += '<body><div class="sidenav">'
    html_code += '<ul id="myUL">'
    cur_path = path
    for (dirpath, dirnames, filenames) in tree:
        dirpath = dirpath.replace('\\\\', '\\')
        print(dirpath)
        depth_diff = path_depth(cur_path) - path_depth(dirpath)
        if depth_diff == 0 and cur_path != path:
            html_code += '</li>'
        else:
            while depth_diff > 0:
                html_code +='</li>'
                html_code += '</ul>'
                depth_diff -= 1
        dir_name = os.path.split(dirpath)[1]
        print('dirpath:' + dirpath + ' dir_name: ' + dir_name)
        html_code += '<li><span class="caret">' + dir_name + '</span>'
        if dirnames or filenames:
            html_code += '<ul class="nested">'
        for filename in filenames:
            html_code += '<li><a href="#">' + filename + '</a></li>'
        cur_path = dirpath
    depth_diff = path_depth(cur_path) - path_depth(path)
    while depth_diff > 0:
        html_code += '</li>'
        html_code += '</ul>'
        depth_diff -= 1
    html_code += '</li></ul>'
    html_code += '</div><script type="text/javascript" src="js/treeView.js"></script></body></html>'

    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()

    h_file = open("web/test.html", "w")
    h_file.write(pretty_html)
    h_file.close()

