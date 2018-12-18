import ast
from Ranker import Ranker
from Parse import Parse
import linecache


class Searcher:

    def __init__(self, corpus_path, posting_path, terms_dict, cities_dict, docs_dict):
        self.terms_dict = terms_dict
        self.cities_dict = cities_dict
        self.docs_dict = docs_dict
        self.parser = Parse(corpus_path)  ## corpus path for stop words
        self.posting_path = posting_path
        self.ranker = Ranker()
        self.model = None
        self.with_semantics = False

    def get_terms_from_post(self, query_terms):
        path = self.posting_path + '\FinalPost' + '\Final_Post'
        query_dict = {}
        for term in query_terms:
            term = str(term)
            if term not in self.terms_dict:
                continue
            line = self.terms_dict[term][0] + 1
            term_index = linecache.getline(path, line)
            term_index = term_index.split('|')[1].split('#')
            i = 0
            while i < len(term_index) - 1:
                term_doc_info = ast.literal_eval(term_index[i])
                for doc in term_doc_info:
                    if term not in query_dict:
                        query_dict[term] = {}
                    query_dict[term][doc] = term_doc_info[doc]
                i += 1
        return query_dict

    def get_five_entities(self, document):
        pass

    def search(self, query):
        self.parser.parsed_doc = None
        query_terms = {}
        if self.with_semantics:
            query = self.parser.main_parser(text=query)
            for word in query:
                synonyms = self.model.wv.most_similar(positive=word)
                for i in range(0, 3):
                    query_terms[(synonyms[i][0]).encode("ascii")] = 1
                query_terms[word] = query[word][0]
        else:
            query = self.parser.main_parser(text=query)
            for word in query:
                query_terms[word] = query[word][0]
        words_terms = self.get_terms_from_post(query_terms)
        result = self.ranker.rank_doc(query_terms, words_terms, self.docs_dict)
        return result


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
