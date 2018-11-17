import pickle


class Indexer:

    def __init__(self, posting_path):
        self.posting_path = posting_path
        self.post_count = 0
        pass

#working indexer
    def index_terms(self, docs_terms_dict, docs):
        terms = {}
        df_dict = {}
        docs_tf_dict = {}
        docs_locations_dict = {}
        terms_docs_dict = {}
        posting_list = []
        for doc in docs:
            for term in docs_terms_dict[doc.id]:
                if not df_dict.__contains__(term):
                    df_dict[term] = docs_terms_dict[doc.id][term][0]
                    docs_locations_dict[term] = {}
                    docs_tf_dict[term] = {}
                    terms_docs_dict[term] = set()
                else:
                    df_dict[term] += docs_terms_dict[doc.id][term][0]
                    terms_docs_dict[term].add(doc.id)
                docs_tf_dict[term][doc.id] = docs_terms_dict[doc.id][term][0]  ## add tf_idf
                docs_locations_dict[term][doc.id] = docs_terms_dict[doc.id][term][1]
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
        for term in df_dict:
            posting_list.append(term + ': ' + str(df_dict[term]) + ', ' + str(docs_tf_dict[term]) + ', ' + str(
                docs_locations_dict[term]))
            # posting_list.append(pickle.dumps([term ,df_dict[term] ,docs_tf_dict[term],docs_locations_dict[term]]))
        self.post(sorted(posting_list))
        '''''
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
        '''

    def post(self, posting_list):
        with open('PostingExample', 'wb') as f:
            # with open('C:\\Users\\ronel\\Desktop\\Search Engine\\SEproject\\Postings\\posting'+str(self.post_count), 'wb') as f:
            pickle.dump(posting_list, f)
        self.post_count += 1


class Term:
    def __init__(self, word, df, docs, docs_tf_dict, locations_dict):
        self.word = word
        self.df = df
        self.docs = docs
        self.docs_tf_dict = docs_tf_dict
        self.locations_dict = locations_dict

    def print_term(self):
        print self.word + ': ' + str(self.df) + ', ' + str(self.docs_tf_dict) + ', ' + str(self.locations_dict)
