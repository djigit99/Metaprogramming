class Content:

    def __init__(self, output_path):
        self.classes = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [],
                        'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [],
                        'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [],
                        'y': [], 'z': []}
        self.interfaces = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [],
                        'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [],
                        'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [],
                        'y': [], 'z': []}
        self.traits = {'a': [], 'b': [], 'c': [], 'd': [], 'e': [], 'f': [], 'g': [], 'h': [],
                        'i': [], 'j': [], 'k': [], 'l': [], 'm': [], 'n': [], 'o': [], 'p': [],
                        'q': [], 'r': [], 's': [], 't': [], 'u': [], 'v': [], 'w': [], 'x': [],
                        'y': [], 'z': []}
        self.output_path = output_path

    def add_class_with(self, char, class_):
        self.classes.get(char).append(class_)

    def get_classes_by(self, char):
        return self.classes[char]

    def add_interface_with(self, char, interface):
        self.interfaces.get(char).append(interface)

    def get_interfaces_by(self, char):
        return self.interfaces[char]

    def add_trait_with(self, char, trait):
        self.traits.get(char).append(trait)

    def get_traits_by(self, char):
        return self.traits[char]

    def get_output_path(self):
        return self.output_path

    def process_namespace(self, namespace):
        for class_ in namespace.get_classes():
            self.add_class_with(Content.get_first_alpha(class_.get_name()), class_)

        for interface in namespace.get_interfaces():
            self.add_interface_with(Content.get_first_alpha(interface.get_name()), interface)

        for trait in namespace.get_traits():
            self.add_trait_with(Content.get_first_alpha(trait.get_name()), trait)

        for nm in namespace.get_child_namespaces():
            self.process_namespace(nm)

    @staticmethod
    def get_first_alpha(str):
        for char in str:
            if char.isalpha():
                return char.lower()
