class Docblock:

    def __init__(self, summary="", description="", tags=[]):
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

    # @param tg_name string tag name (e.g. @param)
    def get_tags_by_name(self, tg_name):
        tags = []
        for tag in self.tags:
            if tag.get_tg_name() == tg_name:
                tags.append(tag)
        return tags
