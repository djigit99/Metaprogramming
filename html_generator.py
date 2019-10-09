import os
import xml.etree.ElementTree as ET


# Walk through path tree
# Add directories/php files to XML file
def walk(path):
    list_of_files = {}
    data = ET.Element('tree')
    for (dirpath, dirnames, filenames) in os.walk(path):

        # Append slash if not exists
        if not dirpath.endswith('\\'):
            dirpath += '\\'

        folder = ET.SubElement(data, 'folder')
        folder.set('name', os.path.split(os.path.split(dirpath)[0])[1])
        for dirname in dirnames:
            dir = ET.SubElement(folder, 'dir')
            dir.text = dirname
        for filename in filenames:
            if filename.endswith('.php'):
                file = ET.SubElement(folder, 'file')
                file.text = filename
                list_of_files[filename] = os.sep.join([dirpath, filename])

    # create a new XML file with the results
    mydata = ET.tostring(data).decode()
    myfile = open("tmp.xml", "w")
    myfile.write(mydata)
    myfile.close()

    return list_of_files


# Generate html docs
def __gen__():
    print(3)

