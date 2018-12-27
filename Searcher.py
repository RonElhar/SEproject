import ast
from Ranker import Ranker
from Parse import Parse
import linecache
import gensim
import Stemmer


class Searcher:
    def __init__(self, corpus_path, posting_path, terms_dict, cities_dict, docs_dict, avg_doc_length, with_stemming,
                 with_semantics):
        self.terms_dict = terms_dict
        self.cities_dict = cities_dict
        self.docs_dict = docs_dict
        self.parser = Parse(corpus_path)  ## corpus path for stop words
        self.parser.to_stem = with_stemming
        self.posting_path = posting_path
        self.ranker = Ranker(avg_doc_length)
        self.model = None
        self.with_semantics = with_semantics
        self.with_stemming = with_stemming

    def get_terms_from_post(self, query_terms, cities):
        if self.with_stemming:
            path = self.posting_path + '\sFinalPost' + '\Final_Post'
        else:
            path = self.posting_path + '\FinalPost' + '\Final_Post'

        word_dict = {}
        updated_query_terms = {}
        for term in query_terms:
            if term not in self.terms_dict:
                term_lower = term.lower()
                term_upper = term.upper()
                if term_lower in self.terms_dict:
                    tmp = query_terms[term]
                    term = term_lower
                    updated_query_terms[term] = tmp
                elif term_upper in self.terms_dict:
                    tmp = query_terms[term]
                    term = term_lower
                    updated_query_terms[term] = tmp
                else:
                    continue
            else:
                updated_query_terms[term] = query_terms[term]
            line = self.terms_dict[term][0] + 1
            term_index = linecache.getline(path, line)
            term_index = term_index.split('|')[1].split('#')
            i = 0
            if len(cities) > 0:
                while i < len(term_index) - 1:
                    term_doc_info = ast.literal_eval(term_index[i])
                    for doc_id in term_doc_info:
                        doc = self.docs_dict[doc_id]
                        if doc.origin_city not in cities:
                            continue
                        if term not in word_dict:
                            word_dict[term] = {}
                        word_dict[term][doc_id] = term_doc_info[doc_id]
                    i += 1
            else:
                while i < len(term_index) - 1:
                    term_doc_info = ast.literal_eval(term_index[i])
                    for doc_id in term_doc_info:
                        if term not in word_dict:
                            word_dict[term] = {}
                        word_dict[term][doc_id] = term_doc_info[doc_id]
                    i += 1
        return updated_query_terms, word_dict

    def get_five_entities(self, document):
        pass

    def search(self, query, cities):
        query_terms = {}
        if self.with_semantics:
            if self.with_stemming:
                stem_query = self.parser.main_parser(text=query, doc=None)
                query = gensim.utils.simple_preprocess(query)
                for word in query:
                    synonyms = self.model.wv.most_similar(positive=word)
                    for i in range(0, 3):
                        stem_word = str(self.parser.pystemmer.stemWord((synonyms[i][0]).encode("ascii")))
                        query_terms[stem_word] = 1
                    for stem in stem_query:
                        if stem.lower() in query_terms or stem.upper() in query_terms:
                            continue
                        query_terms[stem] = stem_query[stem][0]
            else:
                query = self.parser.main_parser(text=query, doc=None)
                for word in query:
                    synonyms = self.model.wv.most_similar(positive=word)
                    for i in range(0, 3):
                        query_terms[(synonyms[i][0]).encode("ascii")] = 1
                    query_terms[word] = query[word][0]
        else:
            query = self.parser.main_parser(text=query, doc=None)
            for word in query:
                query_terms[word] = query[word][0]
        query_terms, words_terms = self.get_terms_from_post(query_terms, cities)
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
