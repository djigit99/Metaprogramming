class Docblock:

    def __init__(self, summary = "", description = "", tags = []):
        self.summary = summary
        self.description = description
        self.tags = tags

    def get_summary(self):
        return self.summary

    def get_description(self):
        return self.description

    def add_tag(self, tag):
        self.tags.append(tag)

    def get_tags(self):
        return self.tags

    def get_tag_by_name(self, tg_name):
        for tag in self.tags:
            if tag.get_tg_name() == tg_name:
                return tag
