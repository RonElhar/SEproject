import sys
import pickle

import os

import CityDetailes
import cPickle
from timeit import default_timer as timer

import Parse

del_size = sys.getsizeof('\n')


class Indexer:

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
        file_name = '\\Posting' + str(self.post_count) if not self.to_stem else '\\sPosting' + str(self.post_count)
        with open(self.posting_path + file_name, 'wb') as f:
            for term in terms:
                index = '{}|{}#|{}#\n'.format(term, str(docs_tf_dict[term]), str(docs_locations_dict[term]))
                f.write(index)
                line_count += 1
        self.post_files_lines.append(line_count)
        self.post_count += 1

    def index_cities(self, cities):
        capitals_details = CityDetailes.get_capitals_details()
        lines_count = 0
        for city in cities:
            if Parse.isWord(city):
                city_details = {}
                if city in capitals_details:
                    city_details[city] = capitals_details[city]
                else:
                    city_details = CityDetailes.get_city_details(city)
                self.cities_dict[city] = [city_details, cities[city], self.terms_dict.get(city)]
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
        if not os.path.exists(self.posting_path + "\\Pointers"):
            os.makedirs(self.posting_path + "\\Pointers")

        if self.to_stem:
            with open(self.posting_path + "\\Pointers\\sTerms Pointers Dictionary", 'wb') as f:
                pickle.dump(self.terms_dict, f)
            with open(self.posting_path + "\\Pointers\\sCities Pointers Dictionary", 'wb') as f:
                pickle.dump(self.cities_dict, f)
            with open(self.posting_path + "\\Pointers\\sDocuments Pointers Dictionary", 'wb') as f:
                pickle.dump(self.docs_dict, f)
            with open(self.posting_path + "\\Pointers\\sLanguages Dictionary", 'wb') as f:
                pickle.dump(languages, f)

        else:
            with open(self.posting_path + "\\Pointers\\Terms Pointers Dictionary", 'wb') as f:
                pickle.dump(self.terms_dict, f)
            with open(self.posting_path + "\\Pointers\\Cities Pointers Dictionary", 'wb') as f:
                pickle.dump(self.cities_dict, f)
            with open(self.posting_path + "\\Pointers\\Documents Pointers Dictionary", 'wb') as f:
                pickle.dump(self.docs_dict, f)
            with open(self.posting_path + "\\Pointers\\Languages Dictionary", 'wb') as f:
                pickle.dump(languages, f)

    def load(self):
        languages = None
        for root, dirs, filenames in os.walk(self.posting_path):
            for filename in filenames:
                if self.to_stem:
                    if filename == 'sTerms Pointers Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.terms_dict = cPickle.load(f)
                    if filename == 'sCities Pointers Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.cities_dict = cPickle.load(f)
                    if filename == 'sDocuments Pointers Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.docs_dict = cPickle.load(f)
                    if filename == 'sLanguages Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            languages = cPickle.load(f)
                else:
                    if filename == 'Terms Pointers Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.terms_dict = cPickle.load(f)
                    if filename == 'Cities Pointers Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.cities_dict = cPickle.load(f)
                    if filename == 'Documents Pointers Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.docs_dict = cPickle.load(f)
                    if filename == 'Languages Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            languages = cPickle.load(f)

        return languages
