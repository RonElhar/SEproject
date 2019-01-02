from Ranker import Ranker
from Parse import Parse
import linecache

"""
~~~~~~~~~~~~~~~~~~~~~~~~  Module Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Module Contains Methods for searching and retrieve document by some query search 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

def string_to_dict(index_string):
    i = 2
    docs_dict = {}
    locations = []
    while i < len(index_string):
        doc_id_start = i
        while index_string[i] != '\'':
            i += 1
        doc_id = index_string[doc_id_start:i]
        i += 3  # go over ':' and '['
        c = index_string[i]
        tf_start = i
        while index_string[i] != ',':
            i += 1
        tf = index_string[tf_start: i]
        i += 2  # go over ',' and 2nd '['
        while index_string[i] != ']':
            loc_start = i
            while index_string[i] != ',' and index_string[i] != ']':
                c = index_string[i]
                i += 1
            loc = index_string[loc_start:i]
            locations.append(loc)
            i += 1
        docs_dict[doc_id] = [int(tf), locations]
        locations = []
        c = index_string[i]
        i += 3  # go over ']]' and next ',' if exists (go to the start of first doc
    return docs_dict


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

    """
       Description :
           This method brings the posting list of all term in the query
       Args:
           param1: query_terms
           param2: cities

        Return:
            parsed query and words dictionary with all the posting lists of all terms in query
    """
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
                    term = term_upper
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
                cities_docs = set()
                for city in cities:
                    if self.cities_dict[city][2] is not None:
                        cities_docs.update(self.cities_dict[city][2])
                while i < len(term_index) - 1:
                    term_doc_info = string_to_dict(term_index[i])
                    for doc_id in term_doc_info:
                        doc = self.docs_dict[doc_id]
                        if doc.origin_city not in cities and doc_id not in cities_docs:
                            continue
                        if term not in word_dict:
                            word_dict[term] = {}
                        word_dict[term][doc_id] = term_doc_info[doc_id]
                    i += 1
            else:
                while i < len(term_index) - 1:
                    term_doc_info = string_to_dict(term_index[i])
                    for doc_id in term_doc_info:
                        if term not in word_dict:
                            word_dict[term] = {}
                        word_dict[term][doc_id] = term_doc_info[doc_id]
                    i += 1
        return updated_query_terms, word_dict

    """
       Description :
           This method make the search of query brings the posting list and call the ranking function,
           for ranking all the retrieved docs in the posting lists filtered by the cities list
       Args:
           param1: query
           param2: cities

        Return:
            list of the 50 most relevant ranking docs
    """
    def search(self, query, cities):
        query_terms = {}
        if self.with_semantics:
            if self.with_stemming:
                self.parser.set_stemming_bool(False)
                stem_query = self.parser.main_parser(text=query, doc=None)
                self.parser.set_stemming_bool(True)
                for word in stem_query:
                    word = word.lower()
                    if not word.isalpha():
                        continue
                    try:
                        synonyms = self.model.wv.most_similar(positive=word)
                    except:
                        continue
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
                    try:
                        synonyms = self.model.wv.most_similar(positive=word)
                    except:
                        continue
                    for i in range(0, 3):
                        query_terms[(synonyms[i][0]).encode("ascii")] = 1
                    query_terms[word] = query[word][0]
        else:
            query = self.parser.main_parser(text=query, doc=None)
            for word in query:
                query_terms[word] = query[word][0]
        query_terms, words_terms = self.get_terms_from_post(query_terms, cities)
        result = self.ranker.rank_doc(query_terms, words_terms, self.docs_dict, 1)
        return result