import ast
import pickle
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
        pass

    # doc-tf{doc.id}
    ##[term] : df,{doc:{tf-idf},{doc-tf},{locations in doc},[docs.id]}
    # {term: {doc:[tf-idf,[locations],isGood]} djfk34kr81y231o4j1873xcx0904326732
    # {term: doc_term_info1, doc_term_info2}
    ### highest tf idf - 10 first docs
    # working indexer
    def index_terms(self, doc_terms_dict, doc):
        self.docs_count += 1
        for term in doc_terms_dict[doc.id]:
            if not self.df_dict.__contains__(term):
                self.df_dict[term] = doc_terms_dict[doc.id][term][0]
                self.docs_locations_dict[term] = {}
                self.docs_tf_dict[term] = {}
                self.terms_docs_dict[term] = []
            else:
                self.df_dict[term] += doc_terms_dict[doc.id][term][0]
            self.terms_docs_dict[term].append(doc.id)
            self.docs_tf_dict[term][doc.id] = doc_terms_dict[doc.id][term][0]  ## add tf_idf
            self.docs_locations_dict[term][doc.id] = doc_terms_dict[doc.id][term][1]
        if self.docs_count == 10:
            self.post()
            self.docs_count = 0
            self.df_dict = {}
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}
            self.terms_docs_dict = {}

    def post(self):
        #start = timer()
        posting_list = []
        for term in self.df_dict:
            posting_list.append(term + '|' + str(self.df_dict[term]) + '|' + str(self.docs_tf_dict[term]) + '|' + str(
                    self.docs_locations_dict[term]) + '|' + str(self.terms_docs_dict[term]))
        with open('PostingExample' + str(self.post_count), 'wb') as f:
            pickle.dump(sorted(posting_list), f)
        self.docs_count += 1
    #end = timer()
    #print("total time: " + str(end - start))

    def read_post(self, path, post_name):
        start = timer()
        with open('PostingExample' + str(0), 'rb') as f:
            my_list = pickle.load(f)
        df_dict = {}
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
            df_dict[term] = ast.literal_eval(item[1])
            #print(df_dict[term])
            tf_dict[term] = ast.literal_eval(item[2])
            #print tf_dict[term]
            loc_dict[term] = ast.literal_eval(item[3])
            #print loc_dict[term]
            docs_dict[term] = ast.literal_eval(item[4])
            #print docs_dict[term]
        end = timer()
        print("total time: " + str(end - start))




class DocTermInfo:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.tf = 0
        self.tf_idf = 0
        self.term_locations = []

    def print_term(self):
        print self.word + ': ' + str(self.df) + ', ' + str(self.docs_tf_dict) + ', ' + str(self.locations_dict)
