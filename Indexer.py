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
        self.post_files_lines=[]

    def index_terms(self, doc_terms_dict, doc_id):
        for term in doc_terms_dict:
            if not self.docs_tf_dict.__contains__(term):
                self.terms_dict[term] = [doc_terms_dict[term][0],1]
                self.docs_locations_dict[term] = {}
                self.docs_tf_dict[term] = {}
            self.terms_dict[term] = [doc_terms_dict[term][0],self.terms_dict[term][0] + 1]
            self.docs_tf_dict[term][doc_id] = doc_terms_dict[term][0]  ## add tf_idf
            self.docs_locations_dict[term][doc_id] = doc_terms_dict[term][1]
        if len(self.docs_tf_dict) > 300000 or self.finished_parse:
            terms = sorted(self.docs_tf_dict.keys())
            self.post(terms, self.docs_tf_dict, self.docs_locations_dict)
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}

    def post(self, terms, docs_tf_dict, docs_locations_dict):
        line_count = 0
        file_name = '\\Posting' + str(self.post_count) if not self.to_stem else 'PostingS'
        with open(self.posting_path + file_name, 'wb') as f:
            for term in terms:
                index = '{}|{}#|{}#\n'.format(term, str(docs_tf_dict[term]), str(docs_locations_dict[term]))
                f.write(index)
                line_count +=1
        self.post_files_lines.append(line_count)
        self.post_count += 1

    def index_cities(self, cities):
        city_tf = {}
        city_locations = {}
        city_details = {}
        with open("cities", 'wb') as f:
            for city in cities:
                city_details = CityDetailes.get_city_details(city)
                city_index = CityIndex(city, city_details, cities[city], self.terms_dict.get(city))
                startbyte = f.tell()
                cPickle.dump(city_index, f)
                endbyte = f.tell()
                self.cities_dict[city] = [startbyte, endbyte]
        f.close()

    def index_docs(self, docs):
        with open(self.posting_path + "Documents", 'ab+') as f:
            for doc in docs:
                startbyte = f.tell()
                cPickle.dump(doc, f)
                endbyte = f.tell()
                self.docs_dict[doc] = [startbyte, endbyte]
        f.close()

    def post_pointers(self):
        with open(self.posting_path + "Post Blocks", 'wb') as f:
            cPickle.dump(self.post_files_blocks, f)
        f.close()
        if self.to_stem:
            with open(self.posting_path + "sTerms Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.terms_dict, f)
        else:
            with open(self.posting_path + "Terms Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.terms_dict, f)
        with open(self.posting_path + "Cities Pointers Dictionary", 'wb') as f:
            cPickle.dump(self.cities_dict, f)
        with open(self.posting_path + "Documents Pointers Dictionary", 'wb') as f:
            cPickle.dump(self.docs_dict, f)

    def load(self):
        with open("Post Blocks", 'rb') as f:
            self.post_files_blocks = cPickle.load(f)
        f.close()
        if self.to_stem:
            with open("sTerms Pointers Dictionary", 'rb') as f:
                self.terms_dict = cPickle.load(f)
        else:
            with open("Terms Pointers Dictionary", 'rb') as f:
                self.terms_dict = cPickle.load(f)
        f.close()
        with open("Cities Pointers Dictionary", 'rb') as f:
            self.cities_dict = cPickle.load(f)
        with open("Documents Pointers Dictionary", 'rb') as f:
            self.docs_dict = cPickle.load(f)

    def read_city(self, city_name):
        doc = None
        with open("Cities", 'rb') as f:
            f.seek(self.cities_dict[city_name][0])
            data = f.read(self.cities_dict[city_name][1])
            doc = cPickle.loads(data)
        return doc

    def read_doc(self, doc_id):
        doc = None
        with open("Documents", 'rb') as f:
            f.seek(self.docs_dict[doc_id][0])
            data = f.read(self.docs_dict[doc_id][1])
            doc = cPickle.loads(data)
        return doc


class CityIndex:
    def __init__(self, city_name, city_details, doc_tags, terms_pointer):
        self.city_name = city_name
        self.city_details = city_details
        self.doc_tags = doc_tags
        self.terms_pointer = terms_pointer
