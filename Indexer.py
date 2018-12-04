import ast
import sys
import threading
import zlib
import math
from guppy import hpy
import os

import CityDetailes
import cPickle
from timeit import default_timer as timer

import Parse

del_size = sys.getsizeof('\n')


class Indexer:
    city_details_vals = {0: "City", 1: "Country", 2: "Currency", 3: "Population"}

    def __init__(self, posting_path):
        self.posting_path = posting_path
        self.docs_tf_dict = {}
        self.docs_locations_dict = {}
        self.post_count = 0
        self.terms_dict = {}
        self.cities_dict = {}
        self.docs_dict = {}
        self.finished_parse = False
        self.to_stem = False
        self.post_line = 0
        self.post_files_lines = []

    def index_terms(self, doc_terms_dict, doc_id):
        for term in doc_terms_dict:
            if not self.docs_tf_dict.__contains__(term):
                self.terms_dict[term] = [doc_terms_dict[term][0], 1]
                self.docs_locations_dict[term] = {}
                self.docs_tf_dict[term] = {}
            self.terms_dict[term] = [doc_terms_dict[term][0] + self.terms_dict[term][0], self.terms_dict[term][1] + 1]
            self.docs_tf_dict[term][doc_id] = doc_terms_dict[term][0]  ## add tf_idf
            self.docs_locations_dict[term][doc_id] = doc_terms_dict[term][1]

        if len(self.docs_tf_dict) > 30000 or self.finished_parse:
            terms = sorted(self.docs_tf_dict.keys())
            self.post(terms, self.docs_tf_dict, self.docs_locations_dict)
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}

    def post(self, terms, docs_tf_dict, docs_locations_dict):
        line_count = 0
        file_name = '\\Posting' + str(self.post_count) if not self.to_stem else '\\sPosting'+ str(self.post_count)
        with open(self.posting_path + file_name, 'wb') as f:
            for term in terms:
                index = '{}|{}#|{}#\n'.format(term, str(docs_tf_dict[term]), str(docs_locations_dict[term]))
                f.write(index)
                line_count += 1
        self.post_files_lines.append(line_count)
        self.post_count += 1

    def index_cities(self, cities):
        with open(self.posting_path + "\\cities", 'wb') as f:
            lines_count = 0
            for city in cities:
                city_details = CityDetailes.get_city_details(city)
                city_index = '{}|{}|{}|{}\n'.format(city, city_details, cities[city], self.terms_dict.get(city))
                f.write(city_index)
                self.cities_dict[city] = lines_count
                lines_count += 1

    def index_docs(self, docs):
        with open(self.posting_path + "\\Documents", 'wb') as f:
            lines_count = 0
            for doc_id in docs:
                if Parse.isWord(doc_id):
                    doc_index = "{}|{}|{}|{}|{}|{}\n".format(doc_id, docs[doc_id].title, docs[doc_id].origin_city,
                                                             docs[doc_id].num_of_unique_words, docs[doc_id].length,
                                                             docs[doc_id].max_tf)
                    f.write(doc_index)
                    self.docs_dict[doc_id] = lines_count
                    lines_count += 1

    def post_pointers(self, languages):

        if self.to_stem:
            with open(self.posting_path + "\\sTerms Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.terms_dict, f)
            with open(self.posting_path + "\\sCities Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.cities_dict, f)
            with open(self.posting_path + "\\sDocuments Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.docs_dict, f)
            with open(self.posting_path + "\\sLanguages Dictionary", 'wb') as f:
                cPickle.dump(languages, f)

        else:
            with open(self.posting_path + "\\Terms Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.terms_dict, f)
            with open(self.posting_path + "\\Cities Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.cities_dict, f)
            with open(self.posting_path + "\\Documents Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.docs_dict, f)
            with open(self.posting_path + "\\Languages Dictionary", 'wb') as f:
                cPickle.dump(languages, f)

    def load(self):
        languages = None
        if self.to_stem:
            with open("sTerms Pointers Dictionary", 'rb') as f:
                self.terms_dict = cPickle.load(f)
            with open("sCities Pointers Dictionary", 'rb') as f:
                self.cities_dict = cPickle.load(f)
            with open("sDocuments Pointers Dictionary", 'rb') as f:
                self.docs_dict = cPickle.load(f)
            with open(self.posting_path + "Languages Dictionary", 'rb') as f:
                languages = cPickle.load(f)
        else:
            with open("Terms Pointers Dictionary", 'rb') as f:
                self.terms_dict = cPickle.load(f)
            with open("Cities Pointers Dictionary", 'rb') as f:
                self.cities_dict = cPickle.load(f)
            with open("Documents Pointers Dictionary", 'rb') as f:
                self.docs_dict = cPickle.load(f)
            with open(self.posting_path + "Languages Dictionary", 'rb') as f:
                languages = cPickle.load(f)

        return languages
