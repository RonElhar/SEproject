import ast
import pickle
from itertools import chain
from collections import defaultdict
from timeit import default_timer as timer

class Indexer:

    def __init__(self, posting_path):
        self.posting_path = posting_path
        self.docs_count = 0
        self.df_dict = {}
        self.docs_tf_dict = {}
        self.docs_locations_dict = {}
        self.terms_docs_dict = {}
        self.post_count = 0
        self.post_files = []
        pass

    # doc-tf{doc.id}
    ##[term] : df,{doc:{tf-idf},{doc-tf},{locations in doc},[docs.id]}
    # {term: {doc:[tf-idf,[locations],isGood]} djfk34kr81y231o4j1873xcx0904326732
    # {term: doc_term_info1, doc_term_info2}
    ### highest tf idf - 10 first docs
    # working indexer
    def index_terms(self, doc_terms_dict, doc):
        self.docs_count += 1
        for term in doc_terms_dict:
            if not self.docs_tf_dict.__contains__(term):
                self.docs_locations_dict[term] = {}
                self.docs_tf_dict[term] = {}
                self.terms_docs_dict[term] = []
            self.terms_docs_dict[term].append(doc.id)
            self.docs_tf_dict[term][doc.id] = doc_terms_dict[term][0]  ## add tf_idf
            self.docs_locations_dict[term][doc.id] = doc_terms_dict[term][1]
        if self.docs_count == 10:
            self.post()
            self.post_count += 1
            self.docs_count = 0
            self.df_dict = {}
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}
            self.terms_docs_dict = {}

    def post(self):
        #start = timer()
        posting_list = []
        file_name = 'PostingExample' + str(self.post_count)
        self.post_files.append(file_name)
        for term in self.docs_tf_dict:
            posting_list.append(term + '|' + str(self.docs_tf_dict[term]) + '|' + str(
                    self.docs_locations_dict[term]) + '|' + str(self.terms_docs_dict[term]))
        with open(file_name, 'wb') as f:
            print sorted(posting_list)
            pickle.dump(sorted(posting_list), f)
        self.docs_count += 1
    #end = timer()
    #print("total time: " + str(end - start))

    def post_final(self, terms, tf_dict, loc_dict, docs_dict):
        #start = timer()
        posting_list = []
        file_name = 'FinalExample'
        for term in terms:
            posting_list.append(term + '|' + str(tf_dict[term]) + '|' + str(loc_dict[term]) + '|' + str(
                docs_dict[term]))
        with open(file_name, 'wb') as f:
            pickle.dump(sorted(posting_list), f)

    def read_post(self, post_name):
        #start = timer()
        with open(post_name, 'rb') as f:
            my_list = pickle.load(f)
        tf_dict = {}
        loc_dict = {}
        docs_dict = {}
        c = 0
        terms = []
        for item in my_list:
            item = str.split(item, '|')
            term = item[0]
            #tf_dict[terms[0]]
            terms.append(term)
            tf_dict[term] = ast.literal_eval(item[1])
            #print tf_dict[term]
            loc_dict[term] = ast.literal_eval(item[2])
            #print loc_dict[term]
            docs_dict[term] = ast.literal_eval(item[3])
            #print docs_dict[term]
        #end = timer()
        #print("total time: " + str(end - start))
        return terms, tf_dict, loc_dict, docs_dict

    def merge_posting(self):
        i = 1
        tf_dict = {}
        loc_dict = {}
        docs_dict = {}
        terms_keys = []
        terms1, tf_dict1, loc_dict1, docs_dict1 = self.read_post(self.post_files[0])
        while i < len(self.post_files):
            terms2, tf_dict2, loc_dict2, docs_dict2 = self.read_post(self.post_files[i])
            terms_keys = list(set(terms1 + terms2))
            for key in terms_keys:
                if tf_dict1.__contains__(key) and tf_dict2.__contains__(key):
                    merge_values = tf_dict1[key]
                    merge_values.update(tf_dict2[key])
                    tf_dict[key] = merge_values
                elif tf_dict1.__contains__(key):
                    tf_dict[key] = tf_dict1[key]
                else:
                    tf_dict[key] = tf_dict2[key]

                if loc_dict1.__contains__(key) and loc_dict2.__contains__(key):
                    merge_values = loc_dict1[key]
                    merge_values.update(loc_dict2[key])
                    loc_dict[key] = merge_values
                elif loc_dict1.__contains__(key):
                    loc_dict[key] = loc_dict1[key]
                else:
                    loc_dict[key] = loc_dict2[key]

                if docs_dict1.__contains__(key) and docs_dict2.__contains__(key):
                    merge_values = docs_dict1[key] + docs_dict2[key]
                    docs_dict[key] = merge_values
                elif docs_dict1.__contains__(key):
                    docs_dict[key] = docs_dict1[key]
                else:
                    docs_dict[key] = docs_dict2[key]
            self.post_final(terms_keys, tf_dict, loc_dict, docs_dict)
            i += 1
            terms_keys = []
            tf_dict = {}
            loc_dict = {}
            docs_dict = {}
            terms1, tf_dict1, loc_dict1, docs_dict1 = self.read_post('FinalExample')




class DocTermInfo:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.tf = 0
        self.tf_idf = 0
        self.term_locations = []

    def print_term(self):
        print self.word + ': ' + str(self.df) + ', ' + str(self.docs_tf_dict) + ', ' + str(self.locations_dict)

'''
while i < len(self.post_files):
    terms2, df_dict2, tf_dict2, loc_dict2, docs_dict2 = self.read_post(self.post_files[i])
    terms_keys = list(set(terms1 + terms2))
    for key in terms_keys:
        if tf_dict1.__contains__(key) and tf_dict2.__contains__(key):
            merge_values = tf_dict1[key]
            merge_values.update(tf_dict2[key])
            tf_dict[key] = merge_values
        elif tf_dict1.__contains__(key):
            tf_dict[key] = tf_dict1[key]
        else:
            tf_dict[key] = tf_dict2[key]
    loc_keys = list(set(loc_dict1.keys() + loc_dict2.keys()))
    for key in loc_keys:
        if loc_dict1.__contains__(key) and loc_dict2.__contains__(key):
            merge_values = loc_dict1[key]
            merge_values.update(loc_dict2[key])
            loc_dict[key] = merge_values
        elif loc_dict1.__contains__(key):
            loc_dict[key] = loc_dict1[key]
        else:
            loc_dict[key] = loc_dict2[key]
    docs_keys = list(set(loc_dict1.keys() + loc_dict2.keys()))
    for key in docs_keys:
        if docs_dict1.__contains__(key) and docs_dict2.__contains__(key):
            merge_values = docs_dict1[key] + docs_dict2[key]
            docs_dict[key] = merge_values
        elif docs_dict1.__contains__(key):
            docs_dict[key] = docs_dict1[key]
        else:
            docs_dict[key] = docs_dict2[key]
    self.post_final(terms, tf_dict, loc_dict, docs_dict)
    terms, df_dict1, tf_dict1, loc_dict1, docs_dict1 = self.read_post('FinalExample')
'''