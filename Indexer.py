import ast
import linecache
import os

import math

import CityDetailes
import cPickle
import Parse

"""
~~~~~~~~~~~~~~~~~~~~~~~~  Module Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Module Contains the Indexer class, its part is to create index files 
    And save the data of the program in files 
    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class Indexer:
    """
       Class Description :
           This Class is used for creating inverted index for terms,
           and index for cities and docs/
           It also used for saving the data of the program in files.
    """
    """
        Description :
            This method is for initializing the indexer properties
    """

    def __init__(self, posting_path):
        self.posting_path = posting_path
        self.post_count = 0
        self.terms_dict = {}
        self.tf_loc_dict = {}
        self.cities_dict = {}
        self.docs_dict = {}
        self.finished_parse = False
        self.to_stem = False
        self.post_line = 0
        self.post_files_lines = []
        self.countries = set()
        self.num_of_capitals = 0
        self.docs_big_letters_words = {}
        self.tf_idf_dict = {}
        self.docs_avg_length = 0

    """
           Description :
               This method creates inverted index in dictionaries form for terms,
               and aggregating the info about the terms, until we are out of memory,
               than it will call post method to save the data in files and 
               clean it from the main memory
           Args:
               param1 : Parsed terms of a document
               param2 : The document id 

    """

    def index_terms(self, doc_terms_dict, doc_id):
        for term in doc_terms_dict:
            if term not in self.terms_dict:
                self.terms_dict[term] = [doc_terms_dict[term][0], 1]
            else:
                self.terms_dict[term] = [doc_terms_dict[term][0] + self.terms_dict[term][0],
                                         self.terms_dict[term][1] + 1]
            if term not in self.tf_loc_dict:
                self.tf_loc_dict[term] = {}
            self.tf_loc_dict[term][doc_id] = [doc_terms_dict[term][0], doc_terms_dict[term][1]]
        if len(self.tf_loc_dict) > 350000 or self.finished_parse:
            terms = sorted(self.tf_loc_dict.keys())
            self.post(terms, self.tf_loc_dict)
            self.tf_loc_dict = {}

    """
              Description :
                  This method creates gets Terms' inverted index Dictionary
                  and writes them to a file () 
              Args:
                  param1 : Sorted Parsed terms of a document
                  param2 : inverted index Dictionaries 

    """

    def post(self, terms, tf_loc_dict):
        line_count = 0
        file_name = '\\Posting' + str(self.post_count) if not self.to_stem else '\\sPosting' + str(self.post_count)
        with open(self.posting_path + file_name, 'wb') as f:
            for term in terms:
                index = '{}|{}#\n'.format(term, str(tf_loc_dict[term]).replace(' ', ''))
                f.write(index)
                line_count += 1
        self.post_files_lines.append(line_count)
        self.post_count += 1

    """
              Description :
                  This method creates gets Terms' inverted index Dictionary
                  and writes them to a file () 
              Args:
                  param1 : Sorted Parsed terms of a document
                  param2 : inverted index Dictionaries 

    """

    def index_cities(self, cities):
        capitals_details = CityDetailes.get_capitals_details()
        lines_count = 0
        for city in cities:
            if Parse.isWord(city):
                city_details = None
                if city in capitals_details:
                    city_details = capitals_details[city]
                    self.countries.add(city_details["Country"])
                    self.num_of_capitals += 1
                else:
                    city_details = CityDetailes.get_city_details(city)
                    if not city_details is "" and not city_details is None:
                        self.countries.add(city_details["Country"])
                self.cities_dict[city] = [city_details, cities[city], self.terms_dict.get(city)]
                lines_count += 1

    """
              Description :
                  This method creates gets the document objects of the corpus
                  creates an index for them and writes them to a file () 
              Args:
                  param1 : Dictionary of documents objects
    """

    def index_docs(self, docs):

        length_sum = 0
        with open(self.posting_path + "\\Documents", 'wb') as f:
            lines_count = 0
            for doc_id in docs:
                doc = docs[doc_id]
                length_sum += docs[doc_id].length
                doc_index = "{}|{}|{}|{}|{}|{}\n".format(doc_id, docs[doc_id].title, docs[doc_id].origin_city,
                                                         docs[doc_id].num_of_unique_words, docs[doc_id].max_tf,
                                                         docs[doc_id].five_entities)
                f.write(doc_index)
                self.docs_dict[doc_id] = [lines_count, docs[doc_id].length]
                lines_count += 1
        self.docs_avg_length = length_sum / (len(self.docs_dict))
        print self.docs_avg_length

    """
              Description :
                  This method saves pointers to indexes dictionaries 
                  to files.
              Args:
                  param1 : languages
    """

    def post_pointers(self, languages):
        if not os.path.exists(self.posting_path + "\\Pointers"):
            os.makedirs(self.posting_path + "\\Pointers")

        tmp_dict = {}
        for term in self.terms_dict.keys():
            tmp_dict[term] = [self.terms_dict[term][0], self.terms_dict[term][1], self.terms_dict[term][2]]
        self.terms_dict = tmp_dict

        if self.to_stem:
            with open(self.posting_path + "\\Pointers\\sTerms Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.terms_dict, f)
            with open(self.posting_path + "\\Pointers\\sCities Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.cities_dict, f)
            with open(self.posting_path + "\\Pointers\\sDocuments Dictionary", 'wb') as f:
                cPickle.dump(self.docs_dict, f)
            with open(self.posting_path + "\\Pointers\\sAvg Doc Length", 'wb') as f:
                cPickle.dump(self.docs_avg_length, f)
            with open(self.posting_path + "\\Pointers\\sLanguages Dictionary", 'wb') as f:
                cPickle.dump(languages, f)

        else:
            with open(self.posting_path + "\\Pointers\\Terms Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.terms_dict, f)
            with open(self.posting_path + "\\Pointers\\Cities Pointers Dictionary", 'wb') as f:
                cPickle.dump(self.cities_dict, f)
            with open(self.posting_path + "\\Pointers\\Documents Dictionary", 'wb') as f:
                cPickle.dump(self.docs_dict, f)
            with open(self.posting_path + "\\Pointers\\Avg Doc Length", 'wb') as f:
                cPickle.dump(self.docs_avg_length, f)
            with open(self.posting_path + "\\Pointers\\Languages Dictionary", 'wb') as f:
                cPickle.dump(languages, f)

    def calculate_tf_idf(self):
        terms = sorted(self.terms_dict.keys())
        path = self.posting_path + '\FinalPost' + '\Final_Post'
        term_count = 0
        term = terms[0]
        while term[0] < 'A':
            term_count += 1
            term = terms[term_count]
        while term[0] <= 'Z':
            tf_idf = 0
            line = self.terms_dict[term][0] + 1
            term_line = linecache.getline(path, line)
            term_docs = term_line.split('|')[1].split('#')
            df = self.terms_dict[term][2]
            i = 0
            while i < len(term_docs) - 1:
                term_doc_info = ast.literal_eval(term_docs[i])
                doc = term_doc_info.keys()[0]
                tf = term_doc_info[doc][1]
                tf_idf = (
                        (float(tf) / self.docs_dict[doc][1]) * (math.log10(len(self.docs_dict) / float(df))))
                if not doc in self.tf_idf_dict:
                    self.tf_idf_dict[doc] = {}
                self.tf_idf_dict[doc][term] = tf_idf
                i += 1

            term_count += 1
            term = terms[term_count]

    """
              Description :
                  This method loads pointers to indexes dictionaries 
                  to the program's memory.

               Returns languages of the corpus 
    """

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
                    if filename == 'sDocuments Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.docs_dict = cPickle.load(f)
                    if filename == 'sAvg Doc Length':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.docs_avg_length = cPickle.load(f)
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
                    if filename == 'Documents Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.docs_dict = cPickle.load(f)
                    if filename == 'Avg Doc Length':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            self.docs_avg_length = cPickle.load(f)
                    if filename == 'Languages Dictionary':
                        filename = os.path.join(root, filename)
                        with open(filename, 'rb') as f:
                            languages = cPickle.load(f)

        return languages
