class SchoolData:

    def __init__(
        self,
        title,
        url,
        content,
        tuition_links,
        admission_links
    ):

        self.title = title

        self.url = url

        self.content = content

        self.tuition_links = tuition_links

        self.admission_links = admission_links

    def to_dict(self):

        return {

            "title": self.title,

            "url": self.url,

            "content": self.content,

            "tuition_links": self.tuition_links,

            "admission_links": self.admission_links
        }