class Tag:

    def __init__(self, tg_name):
        self.tg_name = tg_name

    def get_tg_name(self):
        return self.tg_name


class Tag_Author(Tag):

    def __init__(self, author_name, author_email):
        super().__init__("@author")
        self.author_name = author_name
        self.author_email = author_email

    def set_author_name(self, author_name):
        self.author_name = author_name

    def get_author_name(self):
        return self.author_name

    def set_author_email(self, author_email):
        self.author_email = author_email

    def get_author_email(self):
        return self.author_email


class Tag_Version(Tag):

    def __init__(self, version):
        super().__init__("@version")
        self.version = version

    def set_version(self, version):
        self.version = version

    def get_version(self):
        return self.version


class Tag_Package(Tag):

    def __init__(self, package_name):
        super().__init__("@package")
        self.package_name = package_name

    def set_package_name(self, package_name):
        self.package_name = package_name

    def get_package_name(self):
        return self.package_name

class Tag_Name(Tag):

    def __init__(self, name):
        super().__init__("@name")
        self.name = name

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

class Tag_Global(Tag):

    def __init__(self, type, global_decl):
        super().__init__("@global")
        self.type = type
        self.global_decl = global_decl

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_global_decl(self, global_decl):
        self.global_decl = global_decl

    def get_global_decl(self):
        return self.get_global_decl()


class Tag_Param(Tag):

    def __init__(self, type, name, description):
        super().__init__("@param")
        self.type = type
        self.name = name
        self.description = description

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description


class Tag_Return(Tag):

    def __init__(self, type, description):
        super().__init__("@return")
        self.type = type
        self.description = description

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description