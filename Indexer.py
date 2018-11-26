import ast
import sys
import zlib
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
        self.compressed_block = ''
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
        #print str(self.docs_count) +' : ' + str(self.i)
        # if sys.getsizeof(self.docs_locations_dict)>1024 ** 4:
        #  if (self.i < 8 and self.files_count == 180) or (self.i == 8 and self.files_count == 195):
        if self.docs_count > 29532:
            self.i += 1
            terms = sorted(self.docs_tf_dict.keys())
            self.aggregate_indexes(terms, self.docs_tf_dict, self.docs_locations_dict)
            print ('posted - ' + str(self.i))
            self.docs_count = 0
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}

    def aggregate_indexes(self, terms, docs_tf_dict, docs_locations_dict):
        total_size = 0
        for term in terms:
            index = '{}|{}|{}@'.format(term, str(docs_tf_dict[term]), str(docs_locations_dict[term]))
            cur_size = sys.getsizeof(index)
            # compressed_index = cPickle.dumps(index) + '@'
            cur_size = sys.getsizeof(index)
            tmp_block = zlib.compress(self.compressed_block, 5)
            block_size = sys.getsizeof(tmp_block)
            if block_size + cur_size < (8192):
                self.compressed_block += index
                # compressed_block.append(index)
                total_size += cur_size
            else:
                self.compressed_blocks.append(tmp_block)
                self.block_count += 1
                # compressed_block = compressed_index
                self.compressed_block = index
        if self.docs_count * self.i > 118131:
            self.post()
            self.i = 0

    # self.i = 0

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

        ''''

    '''''

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
            decompressed = zlib.compress(block)
            indexes = str.split(decompressed, '@')
            for i in range(0, len(indexes)):
                index = indexes[i]
                index = str.split(index, '|')
                term = index[0]
                terms.append(term)
                tf_dict[term] = ast.literal_eval(index[1])
                loc_dict[term] = ast.literal_eval(index[2])
        # for term in tf_dict.keys():
        #     print (term + ':' + str(tf_dict[term]) + '     ' + str(loc_dict[term]))
        return terms, tf_dict, loc_dict

    def read_post_consecutive(self, post_num, start_block, num_of_blocks):
        tf_dict = {}
        loc_dict = {}
        terms = []
        data_blocks = []
        with open(self.posting_path + 'Posting' + str(post_num), 'rb') as f:
            read_from = self.post_files_blocks[post_num][start_block]
            if start_block + num_of_blocks < len(self.post_files_blocks[post_num]):
                read_to = self.post_files_blocks[post_num][start_block + num_of_blocks]
                f.seek(read_from, 0)
                data_blocks.append(f.read(read_to))
            else:
                f.seek(read_from, 0)
                data_blocks.append(f.read())
        f.close()

        for block in data_blocks:
            indexes = zlib.decompress(block)
            indexes = str.split(indexes, '@')
            for i in range(0, len(indexes) - 1):
                index = str.split(indexes[i], '|')


                term = index[0]
                terms.append(term)
                tf_dict[term] = ast.literal_eval(index[1])
                loc_dict[term] = ast.literal_eval(index[2])
        for term in tf_dict.keys():
            print term + ':' + str(tf_dict[term]) + ' @@@ ' + str(loc_dict[term])
        return terms, tf_dict, loc_dict

    def merge_posting(self):
        length = self.post_files_blocks.__len__()
        terms = []
        tf_dicts = []
        loc_dicts = []
        read_blocks = []
        tf_dict = {}
        loc_dict = {}
        terms_keys = []
        checked_terms = []
        num_of_blocks_to_read = 100
        total_num_of_blocks = 0
        for j in range(0, length):
            total_num_of_blocks += self.post_files_blocks[j].__len__()
        for i in range(0, length):
            term, tf_dict, loc_dict = self.read_post_consecutive(i, 0, num_of_blocks_to_read)
            terms.append(term)
            tf_dicts.append(tf_dict)
            loc_dicts.append(loc_dict)
            read_blocks.append(num_of_blocks_to_read)
        min_term = terms[0][terms[0].__len__() - 1]
        min_ind = 0
        block_ind = 0
        while block_ind < total_num_of_blocks:
            curr_length = len(terms)
            for i1 in range(0, curr_length):
                terms_keys += terms[i1]
            terms_keys = sorted(list(set(terms_keys)))
            for i2 in range(0, curr_length):
                terms_list_len = terms[i2].__len__() - 1
                if min_term > terms[i2][terms_list_len]:
                    min_term = terms[i2][terms_list_len]
                    min_ind = i2
            for term in terms_keys:
                if term <= min_term:
                    checked_terms.append(term)
            for key in checked_terms:
                tf_merge_values = {}
                loc_merge_values = {}
                for i3 in range(0, curr_length):
                    if terms[i3].__contains__(key):
                        tf_merge_values.update(tf_dicts[i3][key])
                        loc_merge_values.update(loc_dicts[i3][key])
                tf_dict[key] = tf_merge_values
                loc_dict[key] = loc_merge_values
            self.aggregate_indexes(checked_terms, tf_dict, loc_dict)
            terms_keys = []
            checked_terms = []
            tf_dict = {}
            loc_dict = {}
            block_ind += 1
            if self.post_files_blocks[min_ind].__len__() > read_blocks[min_ind]:
                terms[min_ind], tf_dicts[min_ind], loc_dicts[min_ind] = self.read_post_consecutive(
                    min_ind, read_blocks[min_ind], num_of_blocks_to_read)
                read_blocks[min_ind] += num_of_blocks_to_read
                min_term = terms[min_ind][terms[min_ind].__len__() - 1]
            else:
                if terms.__len__() > 1:
                    terms.__delitem__(min_ind)
                    tf_dicts.__delitem__(min_ind)
                    loc_dicts.__delitem__(min_ind)
                    read_blocks.__delitem__(min_ind)
                else:
                    break