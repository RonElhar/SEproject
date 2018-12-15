from Parse import Parse


class Searcher:

    def __init__(self, corpus_path, posting_path, terms_dict, cities_dict, docs_dict):
        self.terms_dict = terms_dict
        self.cities_dict = cities_dict
        self.docs_dict = docs_dict
        self.parser = Parse(corpus_path)  ## corpus path for stop words
        self.posting_path = posting_path
        self.ranker = ''

        def get_term_from_dict(self,term):
            pass

        def rank_terms(self,terms_and_info):
            pass

        def get_five_entities(self,document):
            pass

        def search(self,querry):
            querry_terms = self.parser.main_parser(text=querry)





parser = Parse('C:\Users\USER\Desktop\SearchEngine')
parser.parsed_doc = None
print parser.main_parser("who wants to live forever?")
