import ast

from Parse import Parse
import linecache


class Searcher:

    def __init__(self, corpus_path, posting_path, terms_dict, cities_dict, docs_dict):
        self.terms_dict = terms_dict
        self.cities_dict = cities_dict
        self.docs_dict = docs_dict
        self.parser = Parse(corpus_path)  ## corpus path for stop words
        self.posting_path = posting_path
        self.ranker = ''

    def get_terms_from_post(self, query_terms):
        f = open(self.posting_path + '\FinalPost' + '\Final_Post', 'rb')
        query_dict = {}
        for term in query_terms:
            term_index = linecache.getline(f, query_terms[term][0])
            term_index = term_index.split('|')[1].split('#')
            i = 0
            while i < len(term_index) - 1:
                term_doc_info = ast.literal_eval(term_index[i])
                doc = term_doc_info.keys()[0]
                if i == 0:
                    query_dict[term] = {}
                query_dict[term][doc] = term_doc_info[doc]
                i += 1
        print query_dict

    def rank_terms(self, terms_and_info):
        pass

    def get_five_entities(self, document):
        pass

    def search(self, query):
        query_terms = self.parser.main_parser(text=query)


parser = Parse('C:\Users\USER\Desktop\SearchEngine')
parser.parsed_doc = None
print parser.main_parser("who wants to live forever?")

''''
query_dict = {}
term = "$30-million"
term_index = "$30-million|{'FBIS3-23':[1,[28726]]}#{'FBIS3-6310':[1,[514]],'FBIS3-6955':[1,[286]],'FBIS3-6279':[1,[514]]}#{'FBIS3-6310':[1,[514]],'FBIS3-6955':[1,[286]],'FBIS3-6279':[1,[514]]}#"
term_index = term_index.split('|')[1].split('#')
i = 0
while i < len(term_index) - 1:
    term_doc_info = ast.literal_eval(term_index[i])
    doc = term_doc_info.keys()[0]
    if i == 0:
        query_dict[term] = {}
    query_dict[term][doc] = term_doc_info[doc]
    i += 1
print query_dict
'''''