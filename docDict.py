
class Document:
    def __init__(self, name="", header="", tokens=[], city=""):
        self.name_of_doc = name
        self.header_of_doc = header
        self.tokens_of_doc = tokens
        self.city_of_doc = city
        self.num_of_tokens = tokens.__len__()

    def set_length(self, num):
        self.tokens_of_doc = num



