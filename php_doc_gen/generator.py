import os
from os import listdir
from os.path import isfile, isdir, join, splitext, basename
from string import ascii_lowercase
from shutil import copyfile
from bs4 import BeautifulSoup
from .items import AccessModifier


def gen_sidebar_file(filename, output_path):
    return '<li><a href="' + os.path.join(output_path, 'docs', filename, filename + '.html') + '">' + filename + '.php</a></li>'


def gen_sidebar_folder(folder_path, output_path):
    html_code = ''
    php_files = [f for f in listdir(folder_path) if isfile(join(folder_path, f)) and splitext(f)[1] == '.php']
    for php_file in php_files:
        html_code += gen_sidebar_file(splitext(php_file)[0], output_path)
    return html_code


def gen_sidebar_folder_rec(folder_path, output_path, is_rec=True):
    html_code = '<li><span class="caret_treeView">' + '</span>' + '<a href="' + os.path.join(output_path, 'docs', basename(output_path) + '.html') + '" class="folder_a">' + basename(folder_path) + '</a>'
    html_code += '<ul class="nested">'
    html_code += gen_sidebar_folder(folder_path, output_path)
    if is_rec:
        folders = [f for f in listdir(folder_path) if isdir(join(folder_path, f)) and f != 'docs']
        for folder in folders:
            html_code += gen_sidebar_folder_rec(join(folder_path, folder), join(output_path, folder))
    html_code += '</ul>'
    html_code += '</li>'
    return html_code


def gen_sidebar(folder_path, output_path, is_rec=True, is_file=False, filename=''):
    js_code = 'document.write(String.raw`\n'
    html_code = '<div class="sidenav">'
    html_code += '<ul id="myUL">'
    if is_file:
        html_code += gen_sidebar_file(filename, output_path)
    else:
        html_code += gen_sidebar_folder_rec(folder_path, output_path, is_rec)
    html_code += '</ul>'
    html_code += '</div>'

    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    js_code += pretty_html + '\n`);'

    try:
        with open(os.path.join(output_path, 'docs', 'js', 'side_bar.js'), "w+") as h_file:
            h_file.write(js_code)
            h_file.close()
    except IOError:
        print('Could not open file!')


def gen_main_page(output_path):
    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs'), 0o777, True)
    finally:
        os.umask(original_umask)
    html_code = """<!DOCTYPE html> 
<html lang="en">
<head>
    <meta charset="UTF-8">

    <link href="css/treeViewSheet.css" rel="stylesheet" media="all"/>
    <link href="css/navbar-fixed-left.css" rel="stylesheet" media="all"/>

    <title>Title</title>

    <script>
    window.onload = function(){
        var now = new Date();
        var time = now.toLocaleDateString();

        document.getElementById('output').innerHTML = time;
    }
    </script>
</head>
<body>

<!-- Page content -->
<div class="main">
    <h1 align="center"><em>by </em>PHP Documentation Generator</h1>
    <h3 align="center">Version: <em>1.0</em></h3>
    <h3 align="center"> Generated date: <em id="output"></em></h3>
</div>
"""
    html_code += " <!-- Sidebar bar -->\n"
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js', 'side_bar.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js', 'treeView.js') + '" ' + 'type="text/javascript"></script>'
    html_code += """
</body>
</html>
"""
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        with open(os.path.join(output_path, 'docs', "index.html"), "w+") as h_file:
            h_file.write(pretty_html)
            h_file.close()
    except IOError:
        print('Could not open file!')\



def gen_folder(read_me, output_path, content):
    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs'), 0o777, True)
    finally:
        os.umask(original_umask)
    html_code = """<!DOCTYPE html> 
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <link href="css/treeViewSheet.css" rel="stylesheet" media="all"/>
            <link href="css/navbar-fixed-left.css" rel="stylesheet" media="all"/>
            <link href="css/template.css" rel="stylesheet" media="all"/>
            <link href="css/bootstrap-combined.no-icons.min.css" rel="stylesheet" media="all"/>
            <title>Title</title>
        </head>
        <body>
        <!-- Page content -->
        <div class="main">
       """
    for line in read_me:
        html_code += line + '<br>'
    html_code += """
                    <footer>
                    <nav>
                    """
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'a.html') + '"> Aa </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'b.html') + '"> Bb </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'c.html') + '"> Cc </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'd.html') + '"> Dd </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'e.html') + '"> Ee </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'f.html') + '"> Ff </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'g.html') + '"> Gg </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'h.html') + '"> Hh </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'i.html') + '"> Ii </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'j.html') + '"> Jj </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'k.html') + '"> Kk </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'l.html') + '"> Ll </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'm.html') + '"> Mm </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'n.html') + '"> Nn </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'o.html') + '"> Oo </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'p.html') + '"> Pp </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'q.html') + '"> Qq </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'r.html') + '"> Rr </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 's.html') + '"> Ss </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 't.html') + '"> Tt </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'u.html') + '"> Uu </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'v.html') + '"> Vv </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'w.html') + '"> Ww </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'x.html') + '"> Xx </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'y.html') + '"> Yy </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'z.html') + '"> Zz </a>'
    html_code += """
                    </nav>
                    </footer>
                </div>
                """
    html_code += " <!-- Sidebar bar -->\n"
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'side_bar.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'treeView.js') + '" ' + 'type="text/javascript"></script>'
    html_code += """
        </body>
        </html>
        """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        with open(os.path.join(output_path, 'docs', basename(output_path) + ".html"), "w+") as h_file:
            h_file.write(pretty_html)
            h_file.close()
    except IOError:
        print('Could not open file!')


def gen_file(root_namespace, folder_path, output_path, content):
    filename = root_namespace.get_filename()
    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', filename), 0o777, True)
    finally:
        os.umask(original_umask)
    html_code = """<!DOCTYPE html> 
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <link href="../css/treeViewSheet.css" rel="stylesheet" media="all"/>
        <link href="../css/navbar-fixed-left.css" rel="stylesheet" media="all"/>
        <link href="../css/template.css" rel="stylesheet" media="all"/>
        <link href="../css/bootstrap-combined.no-icons.min.css" rel="stylesheet" media="all"/>
        <title>Title</title>
    </head>
    <body>
    <!-- Page content -->
    <div class="main">
   <header>
  <nav>
  """
    html_code += "<p>" + folder_path + "</p>\n"
    html_code += '<a href="' + os.path.join(output_path, 'docs', filename, filename + '.html') + '">' + filename + '</a>'
    html_code += """
  </nav>
  </header>
   <div>
   """
    html_code += "<h2>" + filename + '.php' + "</h2>"
    html_code += """
    <table class="table table-hover">
     <thead>
      <tr>
       <td> Name </td>
       <td> Title </td>
       <td> Description </td>
       <td> Version </td>
       <td> Author </td>
       <td> Author email </td>
       <td> Root namespace </td>
      </tr>
     </thead>
     <tbody>
      <tr>
      """
    html_code += "<td> <p>" + filename + ".php" + "</p> </td>"
    html_code += "<td> <em>" + root_namespace.get_title() + "</em> </td>"
    html_code += "<td> <em>" + root_namespace.get_description() + "</em> </td>"
    html_code += "<td> <em>" + root_namespace.get_file_version() + "</em> </td>"
    html_code += "<td> <p>" + root_namespace.get_file_author_name() + "</p> </td>"
    html_code += "<td> <em>" + root_namespace.get_file_author_email() + "</em> </td>"
    html_code += '<td> <a href="' + os.path.join(output_path, 'docs', filename, root_namespace.get_link(),
                                                 (root_namespace.get_name() if root_namespace.get_name() != '/' else 'root_nm') + '.html') + '"> / </a> </td>'
    html_code += """
      </tr>
     </tbody>
    </table>
   </div>
   """
    html_code += """
                <footer>
                <nav>
                """
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'a.html') + '"> Aa </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'b.html') + '"> Bb </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'c.html') + '"> Cc </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'd.html') + '"> Dd </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'e.html') + '"> Ee </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'f.html') + '"> Ff </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'g.html') + '"> Gg </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'h.html') + '"> Hh </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'i.html') + '"> Ii </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'j.html') + '"> Jj </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'k.html') + '"> Kk </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'l.html') + '"> Ll </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'm.html') + '"> Mm </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'n.html') + '"> Nn </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'o.html') + '"> Oo </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'p.html') + '"> Pp </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'q.html') + '"> Qq </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'r.html') + '"> Rr </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 's.html') + '"> Ss </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 't.html') + '"> Tt </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'u.html') + '"> Uu </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'v.html') + '"> Vv </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'w.html') + '"> Ww </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'x.html') + '"> Xx </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'y.html') + '"> Yy </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'z.html') + '"> Zz </a>'
    html_code += """
                </nav>
                </footer>
            </div>
            """
    html_code += " <!-- Sidebar bar -->\n"
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'side_bar.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'treeView.js') + '" ' + 'type="text/javascript"></script>'
    html_code += """
    </body>
    </html>
    """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        with open(os.path.join(output_path, 'docs', filename, filename + ".html"), "w+") as h_file:
            h_file.write(pretty_html)
            h_file.close()
    except IOError:
        print('Could not open file!')


def gen_namespace(namespace, output_path, content):
    folder_path = namespace.get_curpath()
    filename = namespace.get_filename()
    js_code = ""
    html_code = """ <!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8"/>
  """
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'treeViewSheet.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'navbar-fixed-left.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'template.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'bootstrap-combined.no-icons.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'popup.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += """
  <title>
   Title
  </title>
  </head>
  <body>
  <!-- Page content -->
  <div class="main">
  <header>
  <nav>
  """
    html_code += "<p>" + folder_path + "</p>\n"
    html_code += '<a href="' + os.path.join(output_path, 'docs', filename, filename + '.html') + '">' + filename + '</a>'
    html_code += "<p>"
    html_code_namespace_name = ''
    cur_nm = namespace
    while cur_nm is not None:
        html_code_namespace_name = '<a href="' + os.path.join(output_path, 'docs', filename, cur_nm.get_link(), (cur_nm.get_name() if cur_nm.get_name() != '/' else 'root_nm') + '.html') + '">' \
                                   + cur_nm.get_name() + '/' + '</a>' + html_code_namespace_name
        cur_nm = cur_nm.get_parent_namespace()
    html_code += html_code_namespace_name + '</p>'
    html_code += """
  </nav>
  </header>
    """
    html_code += """
    <div>
     <h2>
      Namespaces
     </h2>
     <table class="table table-hover">
       <thead>
         <tr>
           <td> Name </td>
         </tr>
       </thead>
      """
    if len(namespace.get_child_namespaces()):
        html_code += "<tbody>\n"
        for nm in namespace.get_child_namespaces():
            html_code += """
       <tr>
        <td> 
        """
            html_code += '<a href="' + os.path.join(output_path, 'docs', filename, nm.get_link(), nm.get_name() + '.html') + '">' + nm.get_name() + '</a>'
            html_code += """
        </td>
      </tr>
      """
        html_code += "</tbody>\n"
    html_code += """
     </table>
   </div>
   """
    html_code += """ <div>
     <h2>
      Classes
     </h2>
     <table class="table table-hover">
       <thead>
         <tr>
           <td> Name </td>
           <td> Title </td>
           <td> Description </td>
         </tr>
       </thead>
    """
    if len(namespace.get_classes()):
        html_code += "<tbody>\n"
        for class_ in namespace.get_classes():
            html_code += """
       <tr>
        <td>
        """
            html_code += '<a href="' + os.path.join(output_path, 'docs', filename, namespace.get_link(), 'classes', class_.get_name() + '.html') + '">' + class_.get_name() + '</a>'
            html_code += """
        </td>
        <td>
         <em> """ + class_.get_title() + """</em>
        </td>
       <td>
        <em> """ + class_.get_description() + """</em>
       </td>
      </tr>
      """
        html_code += "</tbody>\n"
    html_code += """
    </table>
    </div>"""

    html_code += """ <div>
     <h2>
      Interfaces
     </h2>
     <table class="table table-hover">
       <thead>
         <tr>
           <td> Name </td>
           <td> Title </td>
           <td> Description </td>
         </tr>
       </thead>
       """
    if len(namespace.get_interfaces()):
        html_code += "<tbody>\n"
        for interface in namespace.get_interfaces():
            html_code += """
       <tr>
        <td>
        """
            html_code += '<a href="' + os.path.join(output_path, 'docs', filename, namespace.get_link(), 'interfaces', interface.get_name() + '.html') + '">' + interface.get_name() + '</a>'
            html_code += """
        </td>
        <td>
         <em> """ + interface.get_title() + """</em>
        </td>
       <td>
        <em> """ + interface.get_description() + """</em>
       </td>
       </tr>
        """
        html_code += "</tbody>\n"
    html_code += """
     </table>
   </div>
   """

    html_code += """ <div>
     <h2>
      Traits
     </h2>
     <table class="table table-hover">
       <thead>
         <tr>
           <td> Name </td>
           <td> Title </td>
           <td> Description </td>
         </tr>
       </thead> """
    if len(namespace.get_traits()):
        html_code += "<tbody>\n"
        for trait in namespace.get_traits():
            html_code += """
       <tr>
        <td>
        """
            html_code += '<a href="' + os.path.join(output_path, 'docs', filename, namespace.get_link(), 'traits', trait.get_name() + '.html') + '">' + trait.get_name() + '</a>'
            html_code += """
        </td>
        <td>
         <em> """ + trait.get_title() + """</em>
        </td>
       <td>
        <em> """ + trait.get_description() + """</em>
       </td>
       </tr>"""
        html_code += "</tbody>\n"
    html_code += """
     </table>
   </div>
   """
    if namespace.is_root():
        html_code += """ <div>
         <h2>
          Global vars
         </h2>
         <table class="table table-hover">
           <thead>
             <tr>
               <td> Name </td>
               <td> Title </td>
               <td> Description </td>
               <td> Type </td>
             </tr>
           </thead> """
        if len(namespace.get_global_vars()):
            html_code += "<tbody>\n"
            for global_var in namespace.get_global_vars():
                html_code += """
           <tr>
            <td>
             <p>""" + global_var.get_name() + """</p>
            </td>
            <td>
             <em>""" + global_var.get_title() + """</em>
            </td>
           <td>
            <em> """ + global_var.get_description() + """</em>
           </td>
           <td>
            <em> """ + global_var.get_type() + """</em>
           </td>
           </tr> """
            html_code += "</tbody>\n"
        html_code += """
         </table>
       </div>
   """
    html_code += """<div>
     <h2>
      CONSTANTS
     </h2>
     <table class="table table-hover">
       <thead>
         <tr>
           <td> Name </td>
           <td> Title </td>
           <td> Description </td>
           <td> Value </td>
         </tr>
       </thead>
       """
    if len(namespace.get_constants()):
        html_code += "<tbody>\n"
        for const in namespace.get_constants():
            html_code += """
       <tr>
        <td>
         <p>""" + const.get_name() + """</p>
        </td>
        <td>
         <em>""" + const.get_title() + """</em>
        </td>
       <td>
        <em>""" + const.get_description() + """</em>
       </td>
       <td>
        <em> """ + const.get_value() + """</em>
       </td>
       </tr>
       """
        html_code += "</tbody>\n"
    html_code += """
     </table>
   </div>
   """
    html_code += """ <div>
     <h2>
      Functions
     </h2>
     <table class="table table-hover">
       <thead>
         <tr>
           <td> Name </td>
           <td> Title </td>
           <td> Description </td>
           <td> Parameters </td>
           <td> Return </td>
           <td> Source </td>
         </tr>
       </thead> 
       """
    if len(namespace.get_functions()):
        html_code += "<tbody>\n"
        for function in namespace.get_functions():
            html_code += """
       <tr>
        <td>
         <p>""" + function.get_name() + """()...</p>
        </td>
        <td>
         <em>""" + function.get_title() + """</em>
        </td>
        <td>
         <em>""" + function.get_description() + """</em>
        </td>
        <td>
        """
            for param in function.get_parameters():
                html_code += param.get_name() + " : <em>" + param.get_type() + "</em><br>"
            html_code += """
        </td>
        <td> """
            html_code += function.get_return_type() + """
        </td>
        <td> 
            <p><input type="button" value="<>" id="popup__toggle_""" + (
                namespace.get_name() if namespace.get_name() != '/' else '_') + "_" + function.get_name() + """\" /></p>
        </td>
       </tr>
       """
            js_code += """p__""" + (
                namespace.get_name() if namespace.get_name() != '/' else '_') + "_" + function.get_name() + """ = 
            $('.popup__overlay_""" + (
                           namespace.get_name() if namespace.get_name() != '/' else '_') + "_" + function.get_name() + """')
        $('#popup__toggle_""" + (
                           namespace.get_name() if namespace.get_name() != '/' else '_') + "_" + function.get_name() + """').click(function() {
    p__""" + (namespace.get_name() if namespace.get_name() != '/' else '_') + "_" + function.get_name() + """.css('display', 'block')
})
p__""" + (namespace.get_name() if namespace.get_name() != '/' else '_') + "_" + function.get_name() + """.click(function(event) {
    e = event || window.event
    if (e.target == this) {
        $(p__""" + (namespace.get_name() if namespace.get_name() != '/' else '_') + "_" + function.get_name() + """).css('display', 'none')
    }
})
"""
        html_code += "</tbody>\n"
    html_code += """
     </table>
   </div> """
    if len(namespace.get_functions()):
        for function in namespace.get_functions():
            html_code += """
<div class="popup__overlay popup__overlay_""" + (
                namespace.get_name() if namespace.get_name() != '/' else '_') + "_" + function.get_name() + """\">
    <div class="popup">
        <em>""" + function.source_body_html() + """
        </em>
    </div>
   </div>
   """
    html_code += """
                <footer>
                <nav>
                """
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'a.html') + '"> Aa </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'b.html') + '"> Bb </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'c.html') + '"> Cc </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'd.html') + '"> Dd </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'e.html') + '"> Ee </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'f.html') + '"> Ff </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'g.html') + '"> Gg </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'h.html') + '"> Hh </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'i.html') + '"> Ii </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'j.html') + '"> Jj </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'k.html') + '"> Kk </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'l.html') + '"> Ll </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'm.html') + '"> Mm </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'n.html') + '"> Nn </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'o.html') + '"> Oo </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'p.html') + '"> Pp </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'q.html') + '"> Qq </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'r.html') + '"> Rr </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 's.html') + '"> Ss </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 't.html') + '"> Tt </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'u.html') + '"> Uu </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'v.html') + '"> Vv </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'w.html') + '"> Ww </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'x.html') + '"> Xx </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'y.html') + '"> Yy </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'z.html') + '"> Zz </a>'
    html_code += """
                </nav>
                </footer>
            </div>
            """
    html_code += " <!-- Sidebar bar -->\n"
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'side_bar.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'treeView.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'jquery-1.7.min.js') + '" ' + 'type="text/javascript"></script>'
    # <script type="text/javascript" src="js/popup.js"></script>
    html_code += """
 </body>
</html>
"""
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        with open(
            os.path.join(output_path, 'docs', filename, namespace.get_link(), (namespace.get_name() if namespace.get_name() != '/' else 'root_nm') + '.html'),
            "w+") as h_file:
            h_file.write(pretty_html)
            h_file.close()
    except IOError:
        print('Could not open file!')
    try:
        with open("php_doc_gen/web/js/test_popup.js", "a") as h_file:
            h_file.write(js_code)
            h_file.close()
    except IOError:
        print('Could not open file!')


def gen_class(class_, output_path, content):
    namespace = class_.get_namespace()
    folder_path = namespace.get_curpath()
    filename = namespace.get_filename()
    html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    """
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'treeViewSheet.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'navbar-fixed-left.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'font-awesome.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'template.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'bootstrap-combined.no-icons.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += """

    <title>Title</title>
</head>
  <!-- Page content -->
  <div class="main">
    <header>
      <nav> """
    html_code += "<p>" + folder_path + "</p>\n"
    html_code += '<a href="' + os.path.join(output_path, 'docs', filename, filename + '.html') + '">' + filename + '</a>'
    html_code += "<p>"
    html_code_namespace_name = ''
    cur_nm = namespace
    while cur_nm is not None:
        html_code_namespace_name = '<a href="' + os.path.join(output_path, 'docs', filename, cur_nm.get_link(), (namespace.get_name() if namespace.get_name() != '/' else 'root_nm') + '.html')\
                                   + '">' + cur_nm.get_name() + '/' + '</a>' + html_code_namespace_name
        cur_nm = cur_nm.get_parent_namespace()
    html_code += html_code_namespace_name
    html_code += '<a href="' + os.path.join(output_path, 'docs', filename, namespace.get_link(), 'classes', class_.get_name() + '.html') + '">' + class_.get_name() + '</a>'
    html_code += """
      </nav>
      </header>
        """
    html_code += """ <div id="class_title">
      <h1>""" + class_.get_name() + "</h1>\n"
    if class_.get_inherited_class():
        html_code += "<em>extends</em>\n"
        html_code += class_.get_inherited_class() + "\n"
    if class_.get_inherited_interface():
        html_code += "<em>implements</em>\n"
        html_code += class_.get_inherited_interface() + "\n"

    html_code += """<p><em>""" + class_.get_title() + """</em></p>
      <p>""" + class_.get_description() + """</p>
    </div>
    """

    html_code += """ <section id="summary">
      <h2>Summary</h2>
      <section class="row-fluid heading">
        <section class="span2">
          <a href="#methods">Methods</a>
        </section>
        <section class="span2">
          <a href="#properties">Properties</a>
        </section>
        <section class="span2">
          <a href="#constants">Constants</a>
        </section>
      </section> 
      """

    html_code += "<section class=\"row-fluid public\">"
    html_code += "<section class=\"span2\">\n"
    public_methods = class_.get_methods_with_mode(AccessModifier.public)
    if len(public_methods) > 0:
        for method in public_methods:
            html_code += "<a href=\"#method_" + method.get_name() + "\">" + method.get_name() + "()</a><br>\n"
    else:
        html_code += "<em>No public methods found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    public_properties = class_.get_properties_with_mode(AccessModifier.public)
    if len(public_properties) > 0:
        for property_ in public_properties:
            html_code += "<a href=\"#property_" + property_.get_name() + "\">" + property_.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No public properties found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    public_constants = class_.get_constants_with_mode(AccessModifier.public)
    if len(public_constants) > 0:
        for constant in public_constants:
            html_code += "<a href=\"#constant_" + constant.get_name() + "\">" + constant.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No public constants found</em>\n"
    html_code += "</section>\n"

    html_code += "</section>\n"

    html_code += "<section class=\"row-fluid protected\">"
    html_code += "<section class=\"span2\">\n"
    protected_methods = class_.get_methods_with_mode(AccessModifier.protected)
    if len(protected_methods) > 0:
        for method in protected_methods:
            html_code += "<a href=\"#method_" + method.get_name() + "\">" + method.get_name() + "()</a><br>\n"
    else:
        html_code += "<em>No protected methods found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    protected_properties = class_.get_properties_with_mode(AccessModifier.protected)
    if len(protected_properties) > 0:
        for property_ in protected_properties:
            html_code += "<a href=\"#property_" + property_.get_name() + "\">" + property_.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No protected properties found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    protected_constants = class_.get_constants_with_mode(AccessModifier.protected)
    if len(protected_constants) > 0:
        for constant in protected_constants:
            html_code += "<a href=\"#constant_" + constant.get_name() + "\">" + constant.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No protected constants found</em>\n"
    html_code += "</section>\n"

    html_code += "</section>\n"

    html_code += "<section class=\"row-fluid private\">"
    html_code += "<section class=\"span2\">\n"
    private_methods = class_.get_methods_with_mode(AccessModifier.private)
    if len(private_methods) > 0:
        for method in private_methods:
            html_code += "<a href=\"#method_" + method.get_name() + "\">" + method.get_name() + "()</a><br>\n"
    else:
        html_code += "<em>No private methods found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    private_properties = class_.get_properties_with_mode(AccessModifier.private)
    if len(private_properties) > 0:
        for property_ in private_properties:
            html_code += "<a href=\"#property_" + property_.get_name() + "\">" + property_.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No private properties found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    private_constants = class_.get_constants_with_mode(AccessModifier.private)
    if len(private_constants) > 0:
        for constant in private_constants:
            html_code += "<a href=\"#constant_" + constant.get_name() + "\">" + constant.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No private constants found</em>\n"
    html_code += "</section>\n"

    html_code += "</section>\n"

    html_code += """
    <div class="object_stl">
      <a name="constants"></a>
      <h2>Constants</h2>
      """

    for constant in public_constants:
        html_code += "<a name=\"constant_" + constant.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"public\">" + constant.get_name() + "</h3>\n"
        html_code += "<pre>" + constant.get_value() + "</pre>\n"
        html_code += "</article>\n"

    for constant in protected_constants:
        html_code += "<a name=\"constant_" + constant.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"protected\">" + constant.get_name() + "</h3>\n"
        html_code += "<pre>" + constant.get_value() + "</pre>\n"
        html_code += "</article>\n"

    for constant in private_constants:
        html_code += "<a name=\"constant_" + constant.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"private\">" + constant.get_name() + "</h3>\n"
        html_code += "<pre>" + constant.get_value() + "</pre>\n"
        html_code += "</article>\n"
    html_code += "</div>\n"

    html_code += """<div class="object_stl">
      <a name="properties"></a>
      <h2>Properties</h2>
      """

    for property_ in public_properties:
        html_code += "<a name=\"property_" + property_.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"public\">" + property_.get_name() + "</h3>\n"
        html_code += "<pre>" + property_.get_type() + "</pre>\n"
        html_code += "<em>" + property_.get_description() + "</em>"
        html_code += "</article>\n"

    for property_ in protected_properties:
        html_code += "<a name=\"property_" + property_.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"protected\">" + property_.get_name() + "</h3>\n"
        html_code += "<pre>" + property_.get_type() + "</pre>\n"
        html_code += "<em>" + property_.get_description() + "</em>"
        html_code += "</article>\n"

    for property_ in private_properties:
        html_code += "<a name=\"property_" + property_.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"private\">" + property_.get_name() + "</h3>\n"
        html_code += "<pre>" + property_.get_type() + "</pre>\n"
        html_code += "<em>" + property_.get_description() + "</em>"
        html_code += "</article>\n"

    html_code += "</div>\n"

    html_code += """ <div class="object_stl">
      <a name="methods"></a>
      <h2>Methods</h2>
    """

    for method in public_methods:
        html_code += "<a name=\"method_" + method.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"public\">" + method.get_name() + "</h3>\n"
        html_code += "<pre>" + method.get_name() + "( "
        for param in method.get_parameters():
            html_code += param.get_name() + " : <em>" + param.get_type() + "</em>"
            if method.get_parameters().index(param) != len(method.get_parameters()) -1:
                html_code += ', '
        html_code += " ) : <em>" + method.get_return_type() + "</em></pre>\n"
        html_code += method.get_title() + "<br>\n"
        html_code += "<em>" + method.get_description() + "</em>\n"
        html_code += "</article>\n"

    for method in protected_methods:
        html_code += "<a name=\"method_" + method.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"protected\">" + method.get_name() + "</h3>\n"
        html_code += "<pre>" + method.get_name() + "( "
        for param in method.get_parameters():
            html_code += param.get_name() + " : <em>" + param.get_type() + "</em>, "
        html_code += " )</pre>\n"
        html_code += method.get_title() + "<br>\n"
        html_code += "<em>" + method.get_description() + "</em>\n"
        html_code += "</article>\n"

    for method in private_methods:
        html_code += "<a name=\"method_" + method.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"private\">" + method.get_name() + "</h3>\n"
        html_code += "<pre>" + method.get_name() + "( "
        for param in method.get_parameters():
            html_code += param.get_name() + " : <em>" + param.get_type() + "</em>, "
        html_code += " )</pre>\n"
        html_code += method.get_title() + "<br>\n"
        html_code += "<em>" + method.get_description() + "</em>\n"
        html_code += "</article>\n"

    html_code += "</div>\n"

    html_code += """
                <footer>
                <nav>
                """
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'a.html') + '"> Aa </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'b.html') + '"> Bb </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'c.html') + '"> Cc </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'd.html') + '"> Dd </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'e.html') + '"> Ee </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'f.html') + '"> Ff </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'g.html') + '"> Gg </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'h.html') + '"> Hh </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'i.html') + '"> Ii </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'j.html') + '"> Jj </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'k.html') + '"> Kk </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'l.html') + '"> Ll </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'm.html') + '"> Mm </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'n.html') + '"> Nn </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'o.html') + '"> Oo </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'p.html') + '"> Pp </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'q.html') + '"> Qq </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'r.html') + '"> Rr </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 's.html') + '"> Ss </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 't.html') + '"> Tt </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'u.html') + '"> Uu </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'v.html') + '"> Vv </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'w.html') + '"> Ww </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'x.html') + '"> Xx </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'y.html') + '"> Yy </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'z.html') + '"> Zz </a>'
    html_code += """
                </nav>
                </footer>
            </div>
            """
    html_code += " <!-- Sidebar bar -->\n"
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'side_bar.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'treeView.js') + '" ' + 'type="text/javascript"></script>'
    html_code += """
     </body>
    </html>
    """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        with open(os.path.join(output_path, 'docs', filename, namespace.get_link(), 'classes', class_.get_name() + '.html'), "w+") as h_file:
            h_file.write(pretty_html)
            h_file.close()
    except IOError:
        print('Could not open file!')


def gen_interface(interface, output_path, content):
    namespace = interface.get_namespace()
    folder_path = namespace.get_curpath()
    filename = namespace.get_filename()
    html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    """
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'treeViewSheet.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'navbar-fixed-left.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'font-awesome.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'template.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'bootstrap-combined.no-icons.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += """

    <title>Title</title>
</head>
  <!-- Page content -->
  <div class="main">
    <header>
      <nav> """
    html_code += "<p>" + folder_path + "</p>\n"
    html_code += '<a href="' + os.path.join(output_path, 'docs', filename, filename + '.html') + '">' + filename + '</a>'
    html_code += "<p>"
    html_code_namespace_name = ''
    cur_nm = namespace
    while cur_nm is not None:
        html_code_namespace_name = '<a href="' + os.path.join(output_path, 'docs', filename, cur_nm.get_link(),
                                    (namespace.get_name() if namespace.get_name() != '/' else 'root_nm') + '.html') + '">' \
                                   + cur_nm.get_name() + '/' + '</a>' + html_code_namespace_name
        cur_nm = cur_nm.get_parent_namespace()
    html_code += html_code_namespace_name
    html_code += '<a href="' + os.path.join(output_path, 'docs', filename, namespace.get_link(), 'interfaces', interface.get_name() + '.html') +\
                 '">' + interface.get_name() + '</a>'
    html_code += """
      </nav>
      </header>
        """
    html_code += """ <div id="class_title">
      <h1>""" + interface.get_name() + "</h1>\n"
    if len(interface.get_parents()):
        html_code += "<em>extends</em>\n"
        for parent in interface.get_parents():
            html_code += parent + ", "

    html_code += """
    <p><em>""" + interface.get_title() + """</em></p>
      <p>""" + interface.get_description() + """</p>
    </div>
    """

    html_code += """ <section id="summary">
      <h2>Summary</h2>
      <section class="row-fluid heading">
        <section class="span2">
          <a href="#methods">Methods</a>
        </section>
        <section class="span2">
          <a href="#constants">Constants</a>
        </section>
      </section> 
      """

    html_code += "<section class=\"row-fluid public\">"
    html_code += "<section class=\"span2\">\n"
    public_methods = interface.get_methods()
    if len(public_methods) > 0:
        for method in public_methods:
            html_code += "<a href=\"#method_" + method.get_name() + "\">" + method.get_name() + "()</a><br>\n"
    else:
        html_code += "<em>No public methods found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    public_constants = interface.get_constants()
    if len(public_constants) > 0:
        for constant in public_constants:
            html_code += "<a href=\"#constant_" + constant.get_name() + "\">" + constant.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No public constants found</em>\n"
    html_code += "</section>\n"

    html_code += "</section>\n"

    html_code += """
    <div class="object_stl">
      <a name="constants"></a>
      <h2>Constants</h2>
      """

    for constant in public_constants:
        html_code += "<a name=\"constant_" + constant.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"public\">" + constant.get_name() + "</h3>\n"
        html_code += "<pre>" + constant.get_value() + "</pre>\n"
        html_code += "</article>\n"

    html_code += "</div>\n"

    html_code += """ <div class="object_stl">
      <a name="methods"></a>
      <h2>Methods</h2>
    """

    for method in public_methods:
        html_code += "<a name=\"method_" + method.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"public\">" + method.get_name() + "</h3>\n"
        html_code += "<pre>" + method.get_name() + "( "
        for param in method.get_parameters():
            html_code += param.get_name() + " : <em>" + param.get_type() + "</em>, "
        html_code += " )</pre>\n"
        html_code += method.get_title() + "<br>\n"
        html_code += "<em>" + method.get_description() + "</em>\n"
        html_code += "</article>\n"

    html_code += "</div>\n"

    html_code += """
                <footer>
                <nav>
                """
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'a.html') + '"> Aa </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'b.html') + '"> Bb </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'c.html') + '"> Cc </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'd.html') + '"> Dd </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'e.html') + '"> Ee </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'f.html') + '"> Ff </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'g.html') + '"> Gg </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'h.html') + '"> Hh </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'i.html') + '"> Ii </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'j.html') + '"> Jj </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'k.html') + '"> Kk </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'l.html') + '"> Ll </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'm.html') + '"> Mm </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'n.html') + '"> Nn </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'o.html') + '"> Oo </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'p.html') + '"> Pp </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'q.html') + '"> Qq </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'r.html') + '"> Rr </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 's.html') + '"> Ss </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 't.html') + '"> Tt </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'u.html') + '"> Uu </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'v.html') + '"> Vv </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'w.html') + '"> Ww </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'x.html') + '"> Xx </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'y.html') + '"> Yy </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'z.html') + '"> Zz </a>'
    html_code += """
                </nav>
                </footer>
            </div>
            """
    html_code += " <!-- Sidebar bar -->\n"
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'side_bar.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'treeView.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'jquery-1.7.min.js') + '" ' + 'type="text/javascript"></script>'
    # <script type="text/javascript" src="js/popup.js"></script>
    html_code += """
     </body>
    </html>
    """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        with open(os.path.join(output_path, 'docs', filename, namespace.get_link(), 'interfaces', interface.get_name() + '.html'), "w+") as h_file:
            h_file.write(pretty_html)
            h_file.close()
    except IOError:
        print('Could not open file!')


def gen_trait(trait, output_path, content):
    namespace = trait.get_namespace()
    folder_path = namespace.get_curpath()
    filename = namespace.get_filename()
    html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    """
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'treeViewSheet.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'navbar-fixed-left.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'font-awesome.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'template.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'bootstrap-combined.no-icons.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += """

    <title>Title</title>
</head>
  <!-- Page content -->
  <div class="main">
    <header>
      <nav> """
    html_code += "<p>" + folder_path + "</p>\n"
    html_code += '<a href="' + os.path.join(output_path, 'docs', filename, filename + '.html') + '">' + filename + '</a>'
    html_code += "<p>"
    html_code_namespace_name = ''
    cur_nm = namespace
    while cur_nm is not None:
        html_code_namespace_name = '<a href="' + os.path.join(output_path, 'docs', filename, cur_nm.get_link(), (namespace.get_name() if namespace.get_name() != '/' else 'root_nm') + '.html') + '">' \
                                   + cur_nm.get_name() + '/' + '</a>' + html_code_namespace_name
        cur_nm = cur_nm.get_parent_namespace()
    html_code += html_code_namespace_name
    html_code += '<a href="' + os.path.join(output_path, 'docs', filename, namespace.get_link(), 'traits', trait.get_name() + '.html') + '">' + trait.get_name() + '</a>'
    html_code += """
      </nav>
      </header>
        """
    html_code += """ <div id="class_title">
      <h1>""" + trait.get_name() + "</h1>\n"

    html_code += """<p><em>""" + trait.get_title() + """</em></p>
      <p>""" + trait.get_description() + """</p>
    </div>
    """

    html_code += """ <section id="summary">
      <h2>Summary</h2>
      <section class="row-fluid heading">
        <section class="span2">
          <a href="#methods">Methods</a>
        </section>
        <section class="span2">
          <a href="#properties">Properties</a>
        </section>
      </section> 
      """

    html_code += "<section class=\"row-fluid public\">"
    html_code += "<section class=\"span2\">\n"
    public_methods = trait.get_methods_with_mode(AccessModifier.public)
    if len(public_methods) > 0:
        for method in public_methods:
            html_code += "<a href=\"#method_" + method.get_name() + "\">" + method.get_name() + "()</a><br>\n"
    else:
        html_code += "<em>No public methods found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    public_properties = trait.get_properties_with_mode(AccessModifier.public)
    if len(public_properties) > 0:
        for property_ in public_properties:
            html_code += "<a href=\"#property_" + property_.get_name() + "\">" + property_.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No public properties found</em>\n"
    html_code += "</section>\n"

    html_code += "</section>\n"

    html_code += "<section class=\"row-fluid protected\">"
    html_code += "<section class=\"span2\">\n"
    protected_methods = trait.get_methods_with_mode(AccessModifier.protected)
    if len(protected_methods) > 0:
        for method in protected_methods:
            html_code += "<a href=\"#method_" + method.get_name() + "\">" + method.get_name() + "()</a><br>\n"
    else:
        html_code += "<em>No protected methods found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    protected_properties = trait.get_properties_with_mode(AccessModifier.protected)
    if len(protected_properties) > 0:
        for property_ in protected_properties:
            html_code += "<a href=\"#property_" + property_.get_name() + "\">" + property_.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No protected properties found</em>\n"
    html_code += "</section>\n"

    html_code += "</section>\n"

    html_code += "<section class=\"row-fluid private\">"
    html_code += "<section class=\"span2\">\n"
    private_methods = trait.get_methods_with_mode(AccessModifier.private)
    if len(private_methods) > 0:
        for method in private_methods:
            html_code += "<a href=\"#method_" + method.get_name() + "\">" + method.get_name() + "()</a><br>\n"
    else:
        html_code += "<em>No private methods found</em>\n"
    html_code += "</section>\n"

    html_code += "<section class=\"span2\">\n"
    private_properties = trait.get_properties_with_mode(AccessModifier.private)
    if len(private_properties) > 0:
        for property_ in private_properties:
            html_code += "<a href=\"#property_" + property_.get_name() + "\">" + property_.get_name() + "</a><br>\n"
    else:
        html_code += "<em>No private properties found</em>\n"
    html_code += "</section>\n"

    html_code += "</section>\n"

    html_code += """<div class="object_stl">
      <a name="properties"></a>
      <h2>Properties</h2>
      """

    for property_ in public_properties:
        html_code += "<a name=\"property_" + property_.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"public\">" + property_.get_name() + "</h3>\n"
        html_code += "<pre>" + property_.get_type() + "</pre>\n"
        html_code += "</article>\n"

    for property_ in protected_properties:
        html_code += "<a name=\"property_" + property_.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"protected\">" + property_.get_name() + "</h3>\n"
        html_code += "<pre>" + property_.get_type() + "</pre>\n"
        html_code += "</article>\n"

    for property_ in private_properties:
        html_code += "<a name=\"property_" + property_.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"private\">" + property_.get_name() + "</h3>\n"
        html_code += "<pre>" + property_.get_type() + "</pre>\n"
        html_code += "</article>\n"

    html_code += "</div>\n"

    html_code += """ <div class="object_stl">
      <a name="methods"></a>
      <h2>Methods</h2>
    """

    for method in public_methods:
        html_code += "<a name=\"method_" + method.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"public\">" + method.get_name() + "</h3>\n"
        html_code += "<pre>" + method.get_name() + "( "
        for param in method.get_parameters():
            html_code += param.get_name() + " : <em>" + param.get_type() + "</em>, "
        html_code += " )</pre>\n"
        html_code += method.get_title() + "<br>\n"
        html_code += "<em>" + method.get_description() + "</em>\n"
        html_code += "</article>\n"

    for method in protected_methods:
        html_code += "<a name=\"method_" + method.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"protected\">" + method.get_name() + "</h3>\n"
        html_code += "<pre>" + method.get_name() + "( "
        for param in method.get_parameters():
            html_code += param.get_name() + " : <em>" + param.get_type() + "</em>, "
        html_code += " )</pre>\n"
        html_code += method.get_title() + "<br>\n"
        html_code += "<em>" + method.get_description() + "</em>\n"
        html_code += "</article>\n"

    for method in private_methods:
        html_code += "<a name=\"method_" + method.get_name() + "\"></a>\n"
        html_code += "<article>\n"
        html_code += "<h3 class=\"private\">" + method.get_name() + "</h3>\n"
        html_code += "<pre>" + method.get_name() + "( "
        for param in method.get_parameters():
            html_code += param.get_name() + " : <em>" + param.get_type() + "</em>, "
        html_code += " )</pre>\n"
        html_code += method.get_title() + "<br>\n"
        html_code += "<em>" + method.get_description() + "</em>\n"
        html_code += "</article>\n"

    html_code += "</div>\n"

    html_code += """
                <footer>
                <nav>
                """
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'a.html') + '"> Aa </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'b.html') + '"> Bb </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'c.html') + '"> Cc </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'd.html') + '"> Dd </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'e.html') + '"> Ee </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'f.html') + '"> Ff </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'g.html') + '"> Gg </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'h.html') + '"> Hh </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'i.html') + '"> Ii </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'j.html') + '"> Jj </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'k.html') + '"> Kk </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'l.html') + '"> Ll </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'm.html') + '"> Mm </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'n.html') + '"> Nn </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'o.html') + '"> Oo </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'p.html') + '"> Pp </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'q.html') + '"> Qq </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'r.html') + '"> Rr </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 's.html') + '"> Ss </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 't.html') + '"> Tt </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'u.html') + '"> Uu </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'v.html') + '"> Vv </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'w.html') + '"> Ww </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'x.html') + '"> Xx </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'y.html') + '"> Yy </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'z.html') + '"> Zz </a>'
    html_code += """
                </nav>
                </footer>
            </div>
            """
    html_code += " <!-- Sidebar bar -->\n"
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js', 'side_bar.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js', 'treeView.js') + '" ' + 'type="text/javascript"></script>'
    html_code += """
     </body>
    </html>
    """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        with open(os.path.join(output_path, 'docs', filename, namespace.get_link(), 'traits', trait.get_name() + '.html'), "w+") as h_file:
            h_file.write(pretty_html)
            h_file.close()
    except IOError:
        print('Could not open file!')


def gen_content_with(content, char, output_path):
    html_code = r"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8"/>
        """
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'treeViewSheet.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'navbar-fixed-left.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'font-awesome.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'template.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + os.path.join(output_path, 'docs', 'css', 'bootstrap-combined.no-icons.min.css') + '" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += r"""
    <title> Title </title>
    </head>
    <body>
        <!-- Page content -->
        <div class="main">
        """
    html_code += """
            <div>
                <h2> Classes </h2>
                <table class="table table-hover">
                <thead>
                    <tr>
                    <td> Class </td> 
                    <td> Folder </td> 
                    <td> File </td>
                    </tr>
                </thead>
                <tbody>
                """
    if len(content.get_classes_by(char)):
        for class_ in content.get_classes_by(char):
            html_code += "<tr>"
            nm = class_.get_namespace()
            folder_path = nm.get_curpath()
            filename = nm.get_filename()
            output_dir = os.path.join(content.get_output_path(), folder_path[folder_path.find(content.get_dirname()) + len(content.get_dirname())+1:],
                                      'docs', filename, nm.get_link(), 'classes', class_.get_name() + '.html')
            html_code += '<td><a href="' + output_dir + '">' + class_.get_name() + '</a></td>'
            html_code += '<td><p>' + folder_path + '</p></td>'
            html_code += '<td><p>' + filename + '</p></td>'
            html_code += '</tr>'
    html_code += "</tbody></table></div>"
    html_code += """
                <div>
                    <h2> Interfaces </h2>
                    <table class="table table-hover">
                    <thead>
                        <tr>
                        <td> Interface </td> 
                        <td> Folder </td> 
                        <td> File </td>
                        </tr>
                    </thead>
                    <tbody>
                    """
    if len(content.get_interfaces_by(char)):
        for interface in content.get_interfaces_by(char):
            html_code += "<tr>"
            nm = interface.get_namespace()
            folder_path = nm.get_curpath()
            filename = nm.get_filename()
            output_dir = os.path.join(content.get_output_path(), folder_path[
                                                                 folder_path.find(content.get_dirname()) + len(
                                                                     content.get_dirname()) + 1:],
                                      'docs', filename, nm.get_link(), 'interfaces', interface.get_name() + '.html')
            html_code += '<td><a href="' + output_dir + '">' + interface.get_name() + '</a></td>'
            html_code += '<td><p>' + folder_path + '</p></td>'
            html_code += '<td><p>' + filename + '</p></td>'
            html_code += '</tr>'
    html_code += "</tbody></table></div>"
    html_code += """
                <div>
                    <h2> Traits </h2>
                    <table class="table table-hover">
                    <thead>
                        <tr>
                        <td> Trait </td> 
                        <td> Folder </td> 
                        <td> File </td>
                        </tr>
                    </thead>
                    <tbody>
                    """
    if len(content.get_traits_by(char)):
        for trait in content.get_traits_by(char):
            html_code += "<tr>"
            nm = trait.get_namespace()
            folder_path = nm.get_curpath()
            filename = nm.get_filename()
            output_dir = os.path.join(content.get_output_path(), folder_path[
                                                                 folder_path.find(content.get_dirname()) + len(
                                                                     content.get_dirname()) + 1:],
                                      'docs', filename, nm.get_link(), 'traits', trait.get_name() + '.html')
            html_code += '<td><a href="' + output_dir + '">' + trait.get_name() + '</a></td>'
            html_code += '<td><p>' + folder_path + '</p></td>'
            html_code += '<td><p>' + filename + '</p></td>'
            html_code += '</tr>'
    html_code += "</tbody></table></div>"
    html_code += """
            <footer>
            <nav>
            """
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'a.html') + '"> Aa </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'b.html') + '"> Bb </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'c.html') + '"> Cc </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'd.html') + '"> Dd </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'e.html') + '"> Ee </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'f.html') + '"> Ff </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'g.html') + '"> Gg </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'h.html') + '"> Hh </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'i.html') + '"> Ii </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'j.html') + '"> Jj </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'k.html') + '"> Kk </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'l.html') + '"> Ll </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'm.html') + '"> Mm </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'n.html') + '"> Nn </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'o.html') + '"> Oo </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'p.html') + '"> Pp </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'q.html') + '"> Qq </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'r.html') + '"> Rr </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 's.html') + '"> Ss </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 't.html') + '"> Tt </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'u.html') + '"> Uu </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'v.html') + '"> Vv </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'w.html') + '"> Ww </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'x.html') + '"> Xx </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'y.html') + '"> Yy </a> |'
    html_code += '<a href="' + os.path.join(content.get_output_path(), 'docs', 'content_A-Z', 'z.html') + '"> Zz </a>'
    html_code += """
            </nav>
            </footer>
        </div>
        """
    html_code += " <!-- Sidebar bar -->\n"
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'side_bar.js') + '" ' + 'type="text/javascript"></script>'
    html_code += '<script src="' + os.path.join(output_path, 'docs', 'js',
                                                'treeView.js') + '" ' + 'type="text/javascript"></script>'
    html_code += """
    </body>
    </html>
   """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        with open(
                os.path.join(output_path, 'docs', 'content_A-Z', char + '.html'), "w+") as h_file:
            h_file.write(pretty_html)
            h_file.close()
    except IOError:
        print('Could not open file!')


def gen_content(content, output_path):
    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', 'content_A-Z'), 0o777, True)
    finally:
        os.umask(original_umask)
    for char in ascii_lowercase:
        gen_content_with(content, char, output_path)


def gen_preload(folder_path, output_path):
    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', 'css'), 0o777, True)
    finally:
        os.umask(original_umask)
    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', 'js'), 0o777, True)
    finally:
        os.umask(original_umask)
    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', 'font'), 0o777, True)
    finally:
        os.umask(original_umask)

    # Source path

    # css
    source_bootstrap = 'php_doc_gen/web/css/bootstrap-combined.no-icons.min.css'
    source_font = 'php_doc_gen/web/css/font-awesome.min.css'
    source_navbar = 'php_doc_gen/web/css/navbar-fixed-left.css'
    source_popup = 'php_doc_gen/web/css/popup.css'
    source_template = 'php_doc_gen/web/css/template.css'
    source_tree_view = 'php_doc_gen/web/css/treeViewSheet.css'

    # js
    source_jquery = 'php_doc_gen/web/js/jquery-1.7.min.js'
    source_tree_view_js = 'php_doc_gen/web/js/treeView.js'

    # font
    source_font_otf = 'php_doc_gen/web/font/FontAwesome.otf'
    source_font_eot = 'php_doc_gen/web/font/fontawesome-webfont.eot'
    source_font_svg = 'php_doc_gen/web/font/fontawesome-webfont.svg'
    source_font_ttf = 'php_doc_gen/web/font/fontawesome-webfont.ttf'
    source_font_woff = 'php_doc_gen/web/font/fontawesome-webfont.woff'

    # Destination path

    # css
    destination_bootstrap = os.path.join(output_path, 'docs', 'css', 'bootstrap-combined.no-icons.min.css')
    destination_font = os.path.join(output_path, 'docs', 'css', 'font-awesome.min.css')
    destination_navbar = os.path.join(output_path, 'docs', 'css', 'navbar-fixed-left.css')
    destination_popup = os.path.join(output_path, 'docs', 'css', 'popup.css')
    destination_template = os.path.join(output_path, 'docs', 'css', 'template.css')
    destination_tree_view = os.path.join(output_path, 'docs', 'css', 'treeViewSheet.css')

    #js

    destination_jquery = os.path.join(output_path, 'docs', 'js', 'jquery-1.7.min.js')
    destination_tree_view_js = os.path.join(output_path, 'docs', 'js', 'treeView.js')


    # font
    destination_font_otf = os.path.join(output_path, 'docs', 'font', 'FontAwesome.otf')
    destination_font_eot = os.path.join(output_path, 'docs', 'font', 'fontawesome-webfont.eot')
    destination_font_svg = os.path.join(output_path, 'docs', 'font', 'fontawesome-webfont.svg')
    destination_font_ttf = os.path.join(output_path, 'docs', 'font', 'fontawesome-webfont.ttf')
    destination_font_woff = os.path.join(output_path, 'docs', 'font', 'fontawesome-webfont.woff')

    copyfile(source_bootstrap, destination_bootstrap)
    copyfile(source_font, destination_font)
    copyfile(source_navbar, destination_navbar)
    copyfile(source_popup, destination_popup)
    copyfile(source_template, destination_template)
    copyfile(source_tree_view, destination_tree_view)

    copyfile(source_jquery, destination_jquery)
    copyfile(source_tree_view_js, destination_tree_view_js)

    copyfile(source_font_otf, destination_font_otf)
    copyfile(source_font_eot, destination_font_eot)
    copyfile(source_font_svg, destination_font_svg)
    copyfile(source_font_ttf, destination_font_ttf)
    copyfile(source_font_woff, destination_font_woff)


def gen_namespace_hierarchy(namespace, output_path, content):
    filename = namespace.get_filename()
    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', filename, namespace.get_link()), 0o777, True)
    finally:
        os.umask(original_umask)
    gen_namespace(namespace, output_path, content)

    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', filename, namespace.get_link(), 'classes'),
                    0o777, True)
    finally:
        os.umask(original_umask)
    for class_ in namespace.get_classes():
        gen_class(class_, output_path, content)

    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', filename, namespace.get_link(), 'interfaces'),
                    0o777, True)
    finally:
        os.umask(original_umask)
    for interface in namespace.get_interfaces():
        gen_interface(interface, output_path, content)

    try:
        original_umask = os.umask(0)
        os.makedirs(os.path.join(output_path, 'docs', filename, namespace.get_link(), 'traits'),
                    0o777, True)
    finally:
        os.umask(original_umask)
    for trait in namespace.get_traits():
        gen_trait(trait, output_path, content)

    for nm in namespace.get_child_namespaces():
        gen_namespace_hierarchy(nm, output_path, content)

