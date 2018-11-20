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
        self.compressed_block_size = 0
        self.block_count = 0
        self.compressed_indexes = {}
        self.compressed_blocks = []
        self.files_count = 0
        self.i = 0
        self.terms_count
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
        if self.files_count == 114:
            self.i += 1
            self.aggregate_indexes()
            self.files_count = 0
            self.docs_count = 0
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}

    def aggregate_indexes(self):
        terms = sorted(self.docs_tf_dict.keys())
        compressed_block = ''
        for term in terms:
            index = term + '|' + str(self.docs_tf_dict[term]) + '|' + str(self.docs_locations_dict[term])
            compressed_index = cPickle.dumps(index) + '@'
            cur_size = sys.getsizeof(compressed_index)
            block_size = sys.getsizeof(compressed_block)
            if block_size + cur_size < 8192:
                compressed_block += compressed_index
            else:
                self.compressed_blocks.append(compressed_block)
                self.block_count += 1
                compressed_block = compressed_index
        if self.files_count * self.i > 454:
        # self.files_count =0
            self.post()

    def post(self):
        # start = timer()
        file_name = 'Posting' + str(self.post_count)
        self.post_files_blocks.append([])
        self.post_files_blocks[self.post_count].append(0)
        with open(self.posting_path + file_name, 'wb') as f:
            for block in self.compressed_blocks:
                size = sys.getsizeof(block)
                f.write(block)
                self.post_files_blocks[self.post_count].append(f.tell())  #####
        f.close()
        self.compressed_blocks = []
        self.block_count = 0
        self.post_count += 1

    def read_post(self, post_num, block_list):
        # start = timer()
        tf_dict = {}
        loc_dict = {}
        terms = []
        data_blocks = []
        indexes = []
        with open(self.posting_path + 'Posting' + str(post_num), 'rb') as f:
            for block_num in block_list:
                read_from = self.post_files_blocks[post_num][block_num]
                if block_num + 1 < len(self.post_files_blocks[post_num]):
                    read_to = self.post_files_blocks[post_num][block_num + 1]
                    f.seek(read_from, 0)
                    data_blocks.append(f.read(read_to))
                else:
                    f.seek(read_from, 0)
                    data_blocks.append(f.read())
        f.close()

        for block in data_blocks:
            indexes = str.split(block, '@')
            for i in range(0, len(indexes) - 1):
                index = cPickle.loads(indexes[i])
                index = str.split(index, '|')
                term = index[0]
                tf_dict[term] = ast.literal_eval(index[1])
                loc_dict[term] = ast.literal_eval(index[2])
        for term in tf_dict.keys():
            print term + ':' + str(tf_dict[term]) + ' @@@ ' + str(loc_dict[term])

        # end = timer()
        # print("total time: " + str(end - start))
        return terms, tf_dict, loc_dict

    def read_post1(self, post_num, block_list):
        pass

    def merge_posting(self):
        i = 0
        length = len(self.post_files)
        terms = []
        tf_dicts = []
        loc_dicts = []
        docs_dicts = []
        read_blocks = []
        min_ind = -1
        tf_dict = {}
        loc_dict = {}
        docs_dict = {}
        terms_keys = []
        checked_terms = []

        num_of_blocks_to_read = 0
        for i in range(0, length):
            num_of_blocks_to_read += self.post_files_blocks[i]
        for i in range(0, length):  ######### check range func limits
            terms[i], tf_dicts[i], loc_dicts[i], docs_dicts[i] = self.read_post(self.post_files[i], 0)
            read_blocks[i] += 1
        min_term = terms[0][terms[0].__len__()]
        while i < num_of_blocks_to_read:
            curr_length = len(terms)
            for i in range(0, curr_length):
                terms_keys += terms[i]
            terms_keys = sorted(list(set(terms_keys)))
            for i in range(0, curr_length):
                if min_term > terms[i][terms[i].__len__()]:
                    min_term = terms[i][terms[i].__len__()]
                    min_ind = i
            for term in terms_keys:
                if term <= min_term:
                    checked_terms.append(term)
            for key in checked_terms:
                tf_merge_values = {}
                loc_merge_values = {}
                docs_merge_values = {}
                for i in range(0, curr_length):
                    if terms[i].__contains__(key):
                        tf_merge_values.update(tf_dicts[i][key])
                        loc_merge_values.update(loc_dicts[i][key])
                        docs_merge_values.update(docs_dicts[i][key])
                tf_dict[key] = tf_merge_values
                loc_dict[key] = loc_merge_values
                docs_dict[key] = docs_merge_values
            self.post_final(checked_terms, tf_dict, loc_dict, docs_dict)
            terms_keys = []
            checked_terms = []
            tf_dict = {}
            loc_dict = {}
            docs_dict = {}
            i += 1
            if self.post_files_blocks[min_ind] > read_blocks[min_ind]:
                terms[min_ind], tf_dicts[min_ind], loc_dicts[min_ind], docs_dicts[min_ind] = self.read_post(
                    self.post_files[min_ind])
                min_term = terms[0][terms[0].__len__()]
            else:
                if terms.__len__() > 1:
                    terms.__delitem__(min_ind)
                    tf_dicts.__delitem__(min_ind)
                    loc_dicts.__delitem__(min_ind)
                    docs_dicts.__delitem__(min_ind)
                    read_blocks.__delitem__(min_ind)
                else:
                    break

        def post_final(self, terms, tf_dict, loc_dict, docs_dict):
            posting_list = []
            file_name = 'FinalExample'
            for term in terms:
                posting_list.append(term + '|' + str(tf_dict[term]) + '|' + str(loc_dict[term]) + '|' + str(
                    docs_dict[term]))
            with open(file_name, 'wb') as f:
                cPickle.dump(sorted(posting_list), f)
