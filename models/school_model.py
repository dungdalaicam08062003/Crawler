class SchoolData:

    def __init__(
        self,
        title,
        url,
        content,
        html,
        tuition_links,
        admission_links,
        tables,
        links
    ):

        self.title = title
        self.url = url
        self.content = content
        self.html = html
        self.tuition_links = tuition_links
        self.admission_links = admission_links
        self.tables = tables
        self.links = links

    def to_dict(self):

        return {
            "title": self.title,
            "url": self.url,
            "content": self.content,
            "html": self.html,
            "tuition_links": self.tuition_links,
            "admission_links": self.admission_links,
            "tables": self.tables,
            "links": self.links
        }