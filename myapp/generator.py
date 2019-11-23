import os
from bs4 import BeautifulSoup

from myapp.items import AccessModifier


# Find depth of path
def path_depth(path):
    return path.count('\\') + 1


def gen_sidebar(path):
    tree = os.walk(path)
    js_code = 'document.write(`\n'
    html_code = '<div class="sidenav">'
    html_code += '<ul id="myUL">'
    cur_path = path
    for (dirpath, dirnames, filenames) in tree:
        dirpath = dirpath.replace('\\\\', '\\')
        depth_diff = path_depth(cur_path) - path_depth(dirpath)
        if depth_diff == 0 and cur_path != path:
            html_code += '</li>'
        elif depth_diff > 0:
            while depth_diff > 0:
                html_code += '</li>'
                html_code += '</ul>'
                depth_diff -= 1
            html_code += '</li>'
        dir_name = os.path.split(dirpath)[1]
        print('dirpath:' + dirpath)
        html_code += '<li><span class="caret_treeView">' + dir_name + '</span>'
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
    html_code += '</div>'

    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    js_code += pretty_html + '\n`);'

    try:
        h_file = open("web/js/test_side_bar.js", "w+")
    except IOError:
        print('Could not open file!')
    with h_file:
        h_file.write(js_code)
        h_file.close()


def gen_main_page(output_path):
    html_code = r'''<!DOCTYPE html> 
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
<!-- Sidebar bar -->
  <script src="js/test_side_bar.js" type="text/javascript"></script>
  <script src="js/treeView.js" type="text/javascript"></script>


</body>
</html>
'''
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        h_file = open("web/index.html", "w+")
    except IOError:
        print('Could not open file!')
    with h_file:
        h_file.write(pretty_html)
        h_file.close()


def gen_namespace(namespace):
    output_path = namespace.get_curpath()
    filename = namespace.get_filename()
    js_code = ""
    html_code = """ <!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8"/>
  """
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'treeViewSheet.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'navbar-fixed-left.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'template.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'bootstrap-combined.no-icons.min.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'popup.css" ' + 'media="all" rel="stylesheet"/>\n'
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
    html_code += "<p>" + output_path + "</p>\n"
    html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + filename + '.html">' + filename + '</a>'
    html_code += "<p>"
    html_code_namespace_name = ''
    cur_nm = namespace
    while cur_nm is not None:
        html_code_namespace_name = '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + \
                                   '\\' + cur_nm.get_link() + '\\' + cur_nm.get_name() + '.html">' \
                                   + cur_nm.get_name() + '/' + '</a>' + html_code_namespace_name
        cur_nm = cur_nm.get_parent_namespace()
    html_code += html_code_namespace_name
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
            html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + nm.get_link() + '\\' + \
                         nm.get_name() + '.html">' + nm.get_name() + '</a>'
            html_code += """
        </td>
      </tr>
      """
        html_code += "</tbody>\n"
    """
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
            html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() +\
                         '\\' + 'classes' + '\\' + class_.get_name() + '.html">' + class_.get_name() + '</a>'
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
            html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + \
                     '\\' + 'interfaces' + '\\' + interface.get_name() + '.html">' + interface.get_name() + '</a>'
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
            html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + \
                     '\\' + 'traits' + '\\' + trait.get_name() + '.html">' + trait.get_name() + '</a>'
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
    html_code += """ <footer>
     <nav>
       <a href="#">Aa</a> |
       <a href="#">Bb</a> |
       <a href="#">Cc</a> |
       <a href="#">Dd</a> |
       <a href="#">Ee</a> |
       <a href="#">Ff</a> |
       <a href="#">Gg</a> |
       <a href="#">Hh</a> |
       <a href="#">Ii</a> |
       <a href="#">Jj</a> |
       <a href="#">Kk</a> |
       <a href="#">Ll</a> |
       <a href="#">Mm</a> |
       <a href="#">Nn</a> |
       <a href="#">Oo</a> |
       <a href="#">Pp</a> |
       <a href="#">Qq</a> |
       <a href="#">Rr</a> |
       <a href="#">Ss</a> |
       <a href="#">Tt</a> |
       <a href="#">Uu</a> |
       <a href="#">Vv</a> |
       <a href="#">Ww</a> |
       <a href="#">Xx</a> |
       <a href="#">Yy</a> |
       <a href="#">Zz</a>
     </nav>
   </footer>
   """
    html_code += "</div>"
    html_code += """ <!-- Sidebar bar -->
  <script src="js/test_side_bar.js" type="text/javascript"></script>
  <script src="js/treeView.js" type="text/javascript"></script>

  
  <script type="text/javascript" src="js/jquery-1.7.min.js"></script>
  <script type="text/javascript" src="js/test_popup.js"></script>
 </body>
</html>
"""
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        print('path: ' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link())
        h_file = open(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + namespace.get_name() + '.html', "w+")
    except IOError:
        print('Could not open file!')
    with h_file:
        h_file.write(pretty_html)
        h_file.close()
    try:
        h_file = open("web/js/test_popup.js", "a")
    except IOError:
        print('Could not open file!')
    with h_file:
        h_file.write(js_code)
        h_file.close()


def gen_class(class_):
    namespace = class_.get_namespace()
    output_path = namespace.get_curpath()
    filename = namespace.get_filename()
    html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    """
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'treeViewSheet.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'navbar-fixed-left.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'template.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'bootstrap-combined.no-icons.min.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += """

    <title>Title</title>
</head>
  <!-- Page content -->
  <div class="main">
    <header>
      <nav> """
    html_code += "<p>" + output_path + "</p>\n"
    html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + filename + '.html">' + filename + '</a>'
    html_code += "<p>"
    html_code_namespace_name = ''
    cur_nm = namespace
    while cur_nm is not None:
        html_code_namespace_name = '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + \
                                   '\\' + cur_nm.get_link() + '\\' + cur_nm.get_name() + '.html">' \
                                   + cur_nm.get_name() + '/' + '</a>' + html_code_namespace_name
        cur_nm = cur_nm.get_parent_namespace()
    html_code += html_code_namespace_name
    html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' +\
                 'classes' + '\\' + class_.get_name() + '.html">' + class_.get_name() + '</a>'
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

    html_code += """ <footer>
         <nav>
           <a href="#">Aa</a> |
           <a href="#">Bb</a> |
           <a href="#">Cc</a> |
           <a href="#">Dd</a> |
           <a href="#">Ee</a> |
           <a href="#">Ff</a> |
           <a href="#">Gg</a> |
           <a href="#">Hh</a> |
           <a href="#">Ii</a> |
           <a href="#">Jj</a> |
           <a href="#">Kk</a> |
           <a href="#">Ll</a> |
           <a href="#">Mm</a> |
           <a href="#">Nn</a> |
           <a href="#">Oo</a> |
           <a href="#">Pp</a> |
           <a href="#">Qq</a> |
           <a href="#">Rr</a> |
           <a href="#">Ss</a> |
           <a href="#">Tt</a> |
           <a href="#">Uu</a> |
           <a href="#">Vv</a> |
           <a href="#">Ww</a> |
           <a href="#">Xx</a> |
           <a href="#">Yy</a> |
           <a href="#">Zz</a>
         </nav>
       </footer>
       """
    html_code += "</div>"
    html_code += """ <!-- Sidebar bar -->
      <script src="js/test_side_bar.js" type="text/javascript"></script>
      <script src="js/treeView.js" type="text/javascript"></script>


      <script type="text/javascript" src="js/jquery-1.7.min.js"></script>
      <script type="text/javascript" src="js/popup.js"></script>
     </body>
    </html>
    """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        print(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'classes'
                      + '\\' + class_.get_name() + '.html')
        h_file = open(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'classes'
                      + '\\' + class_.get_name() + '.html', "w+")
    except IOError:
        print('Could not open file!')
    with h_file:
        h_file.write(pretty_html)
        h_file.close()


def gen_interface(interface):
    namespace = interface.get_namespace()
    output_path = namespace.get_curpath()
    filename = namespace.get_filename()
    html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    """
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'treeViewSheet.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'navbar-fixed-left.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'template.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'bootstrap-combined.no-icons.min.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += """

    <title>Title</title>
</head>
  <!-- Page content -->
  <div class="main">
    <header>
      <nav> """
    html_code += "<p>" + output_path + "</p>\n"
    html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + filename + '.html">' + filename + '</a>'
    html_code += "<p>"
    html_code_namespace_name = ''
    cur_nm = namespace
    while cur_nm is not None:
        html_code_namespace_name = '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + \
                                   '\\' + cur_nm.get_link() + '\\' + cur_nm.get_name() + '.html">' \
                                   + cur_nm.get_name() + '/' + '</a>' + html_code_namespace_name
        cur_nm = cur_nm.get_parent_namespace()
    html_code += html_code_namespace_name
    html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' +\
                 'interfaces' + '\\' + interface.get_name() + '.html">' + interface.get_name() + '</a>'
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

    html_code += """ <footer>
         <nav>
           <a href="#">Aa</a> |
           <a href="#">Bb</a> |
           <a href="#">Cc</a> |
           <a href="#">Dd</a> |
           <a href="#">Ee</a> |
           <a href="#">Ff</a> |
           <a href="#">Gg</a> |
           <a href="#">Hh</a> |
           <a href="#">Ii</a> |
           <a href="#">Jj</a> |
           <a href="#">Kk</a> |
           <a href="#">Ll</a> |
           <a href="#">Mm</a> |
           <a href="#">Nn</a> |
           <a href="#">Oo</a> |
           <a href="#">Pp</a> |
           <a href="#">Qq</a> |
           <a href="#">Rr</a> |
           <a href="#">Ss</a> |
           <a href="#">Tt</a> |
           <a href="#">Uu</a> |
           <a href="#">Vv</a> |
           <a href="#">Ww</a> |
           <a href="#">Xx</a> |
           <a href="#">Yy</a> |
           <a href="#">Zz</a>
         </nav>
       </footer>
       """
    html_code += "</div>"
    html_code += """ <!-- Sidebar bar -->
      <script src="js/test_side_bar.js" type="text/javascript"></script>
      <script src="js/treeView.js" type="text/javascript"></script>


      <script type="text/javascript" src="js/jquery-1.7.min.js"></script>
      <script type="text/javascript" src="js/popup.js"></script>
     </body>
    </html>
    """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        print(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'interfaces'
                      + '\\' + interface.get_name() + '.html')
        h_file = open(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'interfaces'
                      + '\\' + interface.get_name() + '.html', "w+")
    except IOError:
        print('Could not open file!')
    with h_file:
        h_file.write(pretty_html)
        h_file.close()


def gen_trait(trait):
    namespace = trait.get_namespace()
    output_path = namespace.get_curpath()
    filename = namespace.get_filename()
    html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    """
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'treeViewSheet.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'navbar-fixed-left.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'template.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += '<link href="' + output_path + '\\' + 'docs' + '\\' + 'css' + '\\' + 'bootstrap-combined.no-icons.min.css" ' + 'media="all" rel="stylesheet"/>\n'
    html_code += """

    <title>Title</title>
</head>
  <!-- Page content -->
  <div class="main">
    <header>
      <nav> """
    html_code += "<p>" + output_path + "</p>\n"
    html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + filename + '.html">' + filename + '</a>'
    html_code += "<p>"
    html_code_namespace_name = ''
    cur_nm = namespace
    while cur_nm is not None:
        html_code_namespace_name = '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + \
                                   '\\' + cur_nm.get_link() + '\\' + cur_nm.get_name() + '.html">' \
                                   + cur_nm.get_name() + '/' + '</a>' + html_code_namespace_name
        cur_nm = cur_nm.get_parent_namespace()
    html_code += html_code_namespace_name
    html_code += '<a href="' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' +\
                 'traits' + '\\' + trait.get_name() + '.html">' + trait.get_name() + '</a>'
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

    html_code += """ <footer>
         <nav>
           <a href="#">Aa</a> |
           <a href="#">Bb</a> |
           <a href="#">Cc</a> |
           <a href="#">Dd</a> |
           <a href="#">Ee</a> |
           <a href="#">Ff</a> |
           <a href="#">Gg</a> |
           <a href="#">Hh</a> |
           <a href="#">Ii</a> |
           <a href="#">Jj</a> |
           <a href="#">Kk</a> |
           <a href="#">Ll</a> |
           <a href="#">Mm</a> |
           <a href="#">Nn</a> |
           <a href="#">Oo</a> |
           <a href="#">Pp</a> |
           <a href="#">Qq</a> |
           <a href="#">Rr</a> |
           <a href="#">Ss</a> |
           <a href="#">Tt</a> |
           <a href="#">Uu</a> |
           <a href="#">Vv</a> |
           <a href="#">Ww</a> |
           <a href="#">Xx</a> |
           <a href="#">Yy</a> |
           <a href="#">Zz</a>
         </nav>
       </footer>
       """
    html_code += "</div>"
    html_code += """ <!-- Sidebar bar -->
      <script src="js/test_side_bar.js" type="text/javascript"></script>
      <script src="js/treeView.js" type="text/javascript"></script>


      <script type="text/javascript" src="js/jquery-1.7.min.js"></script>
      <script type="text/javascript" src="js/popup.js"></script>
     </body>
    </html>
    """
    soup = BeautifulSoup(html_code, 'html.parser')  # make BeautifulSoup
    pretty_html = soup.prettify()
    try:
        print(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'traits'
                      + '\\' + trait.get_name() + '.html')
        h_file = open(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'traits'
                      + '\\' + trait.get_name() + '.html', "w+")
    except IOError:
        print('Could not open file!')
    with h_file:
        h_file.write(pretty_html)
        h_file.close()


def gen_hierarchy(folder_path):
    tree = os.walk(folder_path)
    for (dirpath, dirnames, filenames) in tree:
        for filename in filenames:
            os.makedirs(dirpath + '\\docs\\' + filename.split('.')[0], 777, True)


def gen_namespace_hierarchy(namespace):
    output_path = namespace.get_curpath()
    filename = namespace.get_filename()

    print('os:' + output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link())
    os.makedirs(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link(), 777, True)
    gen_namespace(namespace)

    os.makedirs(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'classes',
                777, True)
    for class_ in namespace.get_classes():
        gen_class(class_)

    os.makedirs(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'interfaces',
                777, True)
    for interface in namespace.get_interfaces():
        gen_interface(interface)

    os.makedirs(output_path + '\\' + 'docs' + '\\' + filename + '\\' + namespace.get_link() + '\\' + 'traits',
                777, True)
    for trait in namespace.get_traits():
        gen_trait(trait)

    for nm in namespace.get_child_namespaces():
        gen_namespace_hierarchy(nm)


def main():
    gen_hierarchy(r'D:\recfolder')


if __name__ == '__main__':
    main()
