import pickle


class Indexer:

    def __init__(self, posting_path):
        self.posting_path = posting_path
        self.post_count = 0
        self.df_dict = {}
        self.docs_tf_dict = {}
        self.docs_locations_dict = {}
        self.terms_docs_dict = {}

        pass

    # doc-tf{doc.id}
    ##[term] : df,{doc:{tf-idf},{doc-tf},{locations in doc},[docs.id]}
    # {term: {doc:[tf-idf,[locations],isGood]} djfk34kr81y231o4j1873xcx0904326732
    # {term: doc_term_info1, doc_term_info2}
    ### highest tf idf - 10 first docs
    # working indexer
    def index_terms(self, doc_terms_dict, doc):
        posting_list = []
        for term in doc_terms_dict[doc.id]:
            if not self.df_dict.__contains__(term):
                self.df_dict[term] = doc_terms_dict[doc.id][term][0]
                self.docs_locations_dict[term] = {}
                self.docs_tf_dict[term] = {}
                self.terms_docs_dict[term] = set()
            else:
                self.df_dict[term] += doc_terms_dict[doc.id][term][0]
            self.terms_docs_dict[term].add(doc.id)
            self.docs_tf_dict[term][doc.id] = doc_terms_dict[doc.id][term][0]  ## add tf_idf
            self.docs_locations_dict[term][doc.id] = doc_terms_dict[doc.id][term][1]
            self.post_count += 1
        '''''
        for term in df_dict:
            terms[term] = Term(term, df_dict[term], docs, docs_tf_dict[term], docs_locations_dict[term])
        self.post(terms)
        read_terms = {}
        with open('PostingExample', 'rb') as f:
            read_terms = pickle.load(f)
        for term in sorted(read_terms):
            read_terms[term].print_term()
        '''''
        # posting_list.append(pickle.dumps([term ,df_dict[term] ,docs_tf_dict[term],docs_locations_dict[term]]))
        if self.post_count == 500000:
            self.post()
            self.post_count = 0
            self.df_dict = {}
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}
            self.terms_docs_dict = {}

    # tf_dict = to_dict('{doc1:6 , doc2:3}')
    # loc_dict = {doc1:'[1,2,3,4,5]'
    def post(self):
        posting_list = []
        for term in self.df_dict:
            posting_list.append(term + ': ' + str(self.df_dict[term]) + ',' + str(self.docs_tf_dict[term]) + ',' + str(
                self.docs_locations_dict[term]) + ',' + str(self.terms_docs_dict[term]))
        with open('PostingExample', 'wb') as f:
            # with open('C:\\Users\\ronel\\Desktop\\Search Engine\\SEproject\\Postings\\posting'+str(self.post_count), 'wb') as f:
            pickle.dump(posting_list, f)
        self.post_count += 1

    def read_post(self,path,post_name):
        with open('PostingExample', 'rb') as f:
            my_list = pickle.load(f)
        c = 0
        #print my_list[0]
        for item in my_list:
            if c<500:
                print item
            c+=1
        # item = pickle.loads(my_list[item])
        # print item[0] #+ ': ' + str(item[1][item[0]])# + ', ' + str(item[2][item[0]]) + str(item[3][item[0]])

class DocTermInfo:
    def __init__(self, doc_id):
        self.doc_id = doc_id
        self.tf = 0
        self.tf_idf = 0
        self.term_locations = []

    def print_term(self):
        print self.word + ': ' + str(self.df) + ', ' + str(self.docs_tf_dict) + ', ' + str(self.locations_dict)
