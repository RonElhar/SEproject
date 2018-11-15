import pickle
class Indexer:
    df = 0
    docs_list = 1
    tf = 0
    locations = 1

    def __init__(self,posting_path):
        self.posting_path = posting_path
        pass
    '''
    # prepare string with : term ->
    def index_terms(self,docs_dict,docs):
        terms_dict ={"I":[0,{"",[]}]}
        for doc in docs_dict:
            for term in docs_dict[doc]:
                if not terms_dict.__contains__(term):
                    terms_dict[term]=[]
                    terms_dict[term] = docs_dict[doc][term]
                else:
                    terms_dict[term][Indexer.df] += docs_dict[doc][term][Indexer.df]
                terms_dict[term] = doc
                #terms_dict[term][Indexer.docs_list][doc][Indexer.tf] =  docs_dict[doc][term][Indexer.tf]
                #terms_dict[term][Indexer.docs_list][doc][Indexer.locations] = docs_dict[doc][term][Indexer.locations]
        print(terms_dict)
    '''
    def index_terms1(self,docs_dict,dict):
        df_dict ={}
        docs_tf_dict={}
        location_dict={}
        posting_list = []
        for doc in docs_dict:
            for term in docs_dict[doc]:
                if not df_dict.__contains__(term):
                    df_dict[term] = docs_dict[doc][term]
                else:
                    df_dict[term] += docs_dict[doc][term]
                if not docs_tf_dict.__contains__(term):
                    docs_tf_dict[term] = []
                docs_tf_dict[term].append([doc.id,docs_dict[doc][term]])

        for term in df_dict:
            posting_list.append(term+ ': ' + str(df_dict[term])+ ', ' + str(docs_tf_dict[term]))
        posting_list = sorted(posting_list)
        self.post(posting_list)
        with open('PostingExample', 'rb') as f:
            my_list = pickle.load(f)
        for post in my_list:
            print(post)

    def post(self, posting_list):
        with open('PostingExample', 'wb') as f:
            pickle.dump(posting_list, f)
