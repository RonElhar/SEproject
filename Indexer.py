import ast
import cPickle
import sys
from itertools import chain
from collections import defaultdict
from timeit import default_timer as timer

del_size = sys.getsizeof('\n')


class Indexer:

    def __init__(self, posting_path):
        self.posting_path = posting_path
        self.docs_count = 0
        self.docs_tf_dict = {}
        self.docs_locations_dict = {}
        self.post_count = 0
        self.post_files_blocks = []
        self.compressed_size = 0
        self.block_count = 0
        self.compressed_indexes = {}
        self.compressed_blocks = []
        self.files_count = 0
        # [[]]
        pass

    def index_terms(self, doc_terms_dict, doc):
        for term in doc_terms_dict:
            if not self.docs_tf_dict.__contains__(term):
                self.docs_locations_dict[term] = {}
                self.docs_tf_dict[term] = {}
            self.docs_tf_dict[term][doc.id] = doc_terms_dict[term][0]  ## add tf_idf
            self.docs_locations_dict[term][doc.id] = doc_terms_dict[term][1]
        self.docs_count += 1
        # if sys.getsizeof(self.docs_locations_dict)>1024 ** 4:
        if self.docs_count == 1000:
            self.aggregate_indexes()
            self.docs_count = 0
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}
            self.terms_docs_dict = {}

    def aggregate_indexes(self):
        terms = sorted(self.docs_tf_dict.keys())
        compressed_indexes = ''
        for term in terms:
            index = term + '|' + str(self.docs_tf_dict[term]) + '|' + str(self.docs_locations_dict[term])
            compressed_index = cPickle.dumps(index) + '@'
            cur_size = sys.getsizeof(compressed_index)
            if self.compressed_size + cur_size < (65536):
                compressed_indexes += compressed_index
                self.compressed_size += cur_size
            else:
                self.compressed_blocks.append(compressed_index)
                self.block_count += 1
                self.compressed_size = 0
                compressed_indexes = compressed_index
        self.post()

    def post(self):
        # start = timer()
        file_name = 'Posting' + str(self.post_count)
        self.post_files_blocks.append([])
        self.post_files_blocks[self.post_count].append(0)
        with open(self.posting_path + file_name, 'wb') as f:
            for block in self.compressed_blocks:
                f.write(block)
                self.post_files_blocks[self.post_count].append(f.tell())
        f.close()
        self.compressed_blocks = []
        self.block_count = 0
        self.post_count += 1

    def read_post(self, post_num, block_list):
        # start = timer()
        tf_dict = {}
        loc_dict = {}
        docs_dict = {}
        terms = []
        data_blocks = []
        indexes = []
        with open(self.posting_path + 'Posting' + str(post_num), 'rb') as f:
            for block_num in block_list:
                read_from = self.post_files_blocks[post_num][block_num]
                if block_num + 1 < len(self.post_files_blocks[post_num]):
                    read_to = self.post_files_blocks[post_num][block_num + 1]-1
                    f.seek(read_from, 0)
                    data_blocks.append(f.read(read_to))
                else:
                    f.seek(read_from, 0)
                    data_blocks.append(f.read())
        f.close()

        for block in data_blocks:
            indexes = str.split(block,'@')
            for i in range(0, len(indexes)):
                for index in indexes[i]:
                    index = cPickle.loads(indexes[i])
                    index = str.split(index, '|')
                    term = index[0]
                    tf_dict[term] = ast.literal_eval(index[1])
                    loc_dict[term] = ast.literal_eval(index[2])
        print tf_dict
        print loc_dict
        print docs_dict
        # end = timer()
        # print("total time: " + str(end - start))
        return terms, tf_dict, loc_dict, docs_dict

    def merge_posting(self):
        i = 1
        tf_dict = {}
        loc_dict = {}
        docs_dict = {}
        terms_keys = []
        # blocks0 = []
        # blocks1 = []
        # same_terms = bring_same_valuse(postings[0],postings[1])
        # for term in terms
        #  blocks0.append(posting[0][term])
        #  blocks1.append(posting[1][term])
        #
        # check which blocks to bring by comparing Post files dictionaries
        terms1, tf_dict1, loc_dict1, docs_dict1 = self.read_post(
            self.post_files_blocks[0])  ### get dictionaries of blocks
        while i < len(self.post_files_blocks):
            terms2, tf_dict2, loc_dict2, docs_dict2 = self.read_post(self.post_files_blocks[i])
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

    # def print_term(self):
    #     print self.word + ': ' + str(self.df) + ', ' + str(self.docs_tf_dict) + ', ' + str(self.locations_dict)


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
