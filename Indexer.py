import ast
import sys
import zlib
import math
import CityDetailes
import cPickle
from timeit import default_timer as timer

import Parse

del_size = sys.getsizeof('\n')


class Indexer:
    city_details_vals = {0: "City", 1: "Country", 2: "Currency", 3: "Population"}

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
        self.i = 1
        self.block = ''
        self.num_of_corpus_docs = 472525
        self.terms_dict = {}
        self.pos_in_block = 0
        self.block_size = 0
        self.cities_dict = {}
        self.docs_dict = {}
        self.finished_parse = False
        self.final_count = 0
        self.to_stem = False

    def index_terms(self, doc_terms_dict, doc_id):
        for term in doc_terms_dict:
            if not self.docs_tf_dict.__contains__(term):
                self.terms_dict[term] = None
                self.docs_locations_dict[term] = {}
                self.docs_tf_dict[term] = {}
            self.docs_tf_dict[term][doc_id] = doc_terms_dict[term][0]  ## add tf_idf
            self.docs_locations_dict[term][doc_id] = doc_terms_dict[term][1]
        self.docs_count += 1
        # if sys.getsizeof(self.docs_locations_dict)>1024 ** 4:
        #  if (self.i < 8 and self.files_count == 180) or (self.i == 8 and self.files_count == 195):
        # if (self.docs_count > 29532 and self.post_count < 3) or (
        #         self.docs_count > 29532 and self.post_count == 3 and self.i < 4) or self.finished_parse:  # 29531
        if len(self.docs_tf_dict) > 200000 or self.finished_parse:
            terms = sorted(self.docs_tf_dict.keys())
            self.aggregate_indexes(terms, self.docs_tf_dict, self.docs_locations_dict)
            self.i += 1
            self.docs_count = 0
            self.docs_tf_dict = {}
            self.docs_locations_dict = {}

    def aggregate_indexes(self, terms, docs_tf_dict, docs_locations_dict):
        total_size = 0
        compressed_block = None
        for term in terms:
            index = '{}|{}|{}@'.format(term, str(docs_tf_dict[term]), str(docs_locations_dict[term]))
            cur_size = sys.getsizeof(index)
            # compressed_block = zlib.compress(self.block, 4)
            # block_size = sys.getsizeof(compressed_block)
            if self.block_size + cur_size < 8192:  # 8192
                self.block = "{}{}".format(self.block, index)
                # compressed_block.append(index)
                self.block_size += cur_size
            else:
                compressed_block = zlib.compress(self.block, 4)
                self.block_size = sys.getsizeof(compressed_block)
                if self.block_size + cur_size < 8192:  # 8192
                    self.block = "{}{}".format(self.block, index)
                    self.block_size += cur_size
                else:
                    self.compressed_blocks.append(compressed_block)
                    self.block_count += 1
                    self.block = index
                    self.block_size = cur_size
        # print ('aggregate - ' + str(self.i))
        # if self.docs_count * self.i > 118129 or self.finished_parse:  # 118129
        self.compressed_blocks.append(zlib.compress(self.block, 4))
        self.block = ''
        self.block_size = 0
        self.post()
        self.i = 0

    def post(self):
        # start = timer()
        file_name = '\\Posting' + str(self.post_count) if not self.to_stem else 'PostingS'
        self.post_files_blocks.append([])
        self.post_files_blocks[self.post_count].append(0)
        with open(self.posting_path + file_name, 'wb') as f:
            for block in self.compressed_blocks:
                size = sys.getsizeof(block)
                f.write(block)
                self.post_files_blocks[self.post_count].append(f.tell())  #####
        f.close()
        print("post - " + str(self.post_count))
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
            decompressed = zlib.decompress(block)
            indexes = str.split(decompressed, '@')
            for i in range(0, len(indexes) - 1):
                index = indexes[i]
                index = str.split(index, '|')
                term = index[0]
                terms.append(term)
                tf_dict[term] = ast.literal_eval(index[1])
                loc_dict[term] = ast.literal_eval(index[2])
        for term in tf_dict.keys():
            print (term + ':' + str(tf_dict[term]) + '     ' + str(loc_dict[term]))
        return terms, tf_dict, loc_dict

    def read_post_consecutive(self, post_num, start_block, num_of_blocks):
        tf_dict = {}
        loc_dict = {}
        terms = []
        data_blocks = []
        file_name = 'Posting' if not self.to_stem else 'PostingS'
        with open(self.posting_path + file_name + str(post_num), 'rb') as f:
            i = 0
            while (i < num_of_blocks):
                if not start_block + i < len(self.post_files_blocks[post_num]):
                    break
                read_from = self.post_files_blocks[post_num][start_block + i]
                if start_block + i + 1 < len(self.post_files_blocks[post_num]):
                    read_to = self.post_files_blocks[post_num][start_block + i + 1]
                    f.seek(read_from, 0)
                    data_blocks.append(f.read(read_to))
                else:
                    f.seek(read_from, 0)
                    data_blocks.append(f.read())
                i += 1

        for i in range(0, len(data_blocks) - 1):
            block = data_blocks[i]
            decompressed = zlib.decompress(block)
            indexes = str.split(decompressed, '@')
            for i in range(0, len(indexes) - 1):
                index = indexes[i]
                index = str.split(index, '|')
                term = index[0]
                terms.append(term)
                tf_dict[term] = ast.literal_eval(index[1])
                loc_dict[term] = ast.literal_eval(index[2])
        # for term in tf_dict.keys():
        # print (term + ':' + str(tf_dict[term]) + '     ' + str(loc_dict[term]))
        return terms, tf_dict, loc_dict

    def non_compressed_post_less_memory_use(self):
        for i in range(0, len(self.post_files_blocks) - 1):
            self.non_compressed_final_post(i, len(self.post_files_blocks[i]) - 1)

    def non_compressed_post(self):
        posting_dictionaries = []
        for i in range(0, len(self.post_files_blocks) - 1):
            dict = ''
            dict = self.read_post_consecutive(i, 0, len(self.post_files_blocks[i]) - 1)
            with open(self.posting_path + "TestPost" + str(i), 'wb') as f:
                for term in dict[0]:
                    index = '{}|{}|{}\n'.format(term, str(dict[1][term]), str(dict[2][term]))
                    f.write(index)
            f.close()
        final_index = len(self.post_files_blocks) - 1
        self.non_compressed_final_post(final_index, len(self.post_files_blocks[i]) - 1)

    def non_compressed_final_post(self, post_num, num_of_blocks):
        file_name = '\\Posting' if not self.to_stem else 'PostingS'
        with open(self.posting_path + file_name + str(post_num), 'rb') as f:
            with open(self.posting_path + "TestPost" + str(post_num), 'wb') as f2:
                i = 0
                while i < num_of_blocks:
                    if not i + 1 < len(self.post_files_blocks[post_num]):
                        break
                    read_from = self.post_files_blocks[post_num][i]
                    read_to = self.post_files_blocks[post_num][i + 1]
                    f.seek(read_from, 0)
                    block = f.read(read_to)
                    decompressed = zlib.decompress(block)
                    indexes = str.split(decompressed, '@')
                    for j in range(0, len(indexes) - 1):
                        index = indexes[j]
                        index = str.split(index, '|')
                        term = index[0]
                        index = '{}|{}|{}\n'.format(term, ast.literal_eval(index[1]), ast.literal_eval(index[2]))
                        f2.write(index)
                    i += 1

    def merge_posting(self):
        length = self.post_files_blocks.__len__()
        self.post_files_blocks.append([])
        self.post_files_blocks[self.post_count].append(0)
        big_term = []
        big_tf_dict = {}
        big_loc_dict = {}
        terms = []
        tf_dicts = []
        loc_dicts = []
        read_blocks = []
        all_terms_from_postings = []
        all_terms_to_merge = []
        checked_tf_dict = {}
        checked_loc_dict = {}
        num_of_blocks_to_read = 5
        total_num_of_blocks = 0
        min_blocks = self.post_files_blocks[0].__len__()
        for x in range(1, length):
            if min_blocks > self.post_files_blocks[x].__len__():
                min_blocks = self.post_files_blocks[x].__len__()
        if num_of_blocks_to_read > min_blocks:
            num_of_blocks_to_read = min_blocks
        for j in range(0, length):
            total_num_of_blocks += self.post_files_blocks[j].__len__()
        for i in range(0, length):
            term, tf_dict, loc_dict = self.read_post_consecutive(i, 0, num_of_blocks_to_read)
            terms.append(term)
            tf_dicts.append(tf_dict)
            loc_dicts.append(loc_dict)
            read_blocks.append(num_of_blocks_to_read)
        min_ind = 0
        last_min_term = terms[0][0]
        min_term = terms[0][terms[0].__len__() - 1]
        for i in range(0, length):
            terms_list_len = terms[i].__len__() - 1
            if min_term > terms[i][terms_list_len]:
                last_min_term = terms[i][0]
                min_term = terms[i][terms_list_len]
                min_ind = i
        while True:
            for i1 in range(0, length):
                all_terms_from_postings += terms[i1]
            if all_terms_from_postings.__len__() is 0:
                self.final_posting([], {}, {}, True)
                break
            all_terms_from_postings = sorted(list(set(all_terms_from_postings)))
            for i2 in range(0, length):
                if terms[i2].__len__() > 0:
                    terms_list_len = terms[i2].__len__() - 1
                    if min_term > terms[i2][terms_list_len]:
                        min_term = terms[i2][terms_list_len]
                        min_ind = i2
            for term in all_terms_from_postings:
                if term <= min_term and term > last_min_term:
                    all_terms_to_merge.append(term)
            for key in all_terms_to_merge:
                tf_merge_values = {}
                loc_merge_values = {}
                for i3 in range(0, length):
                    if terms[i3].__len__() > 0:
                        if terms[i3].__contains__(key):
                            tf_merge_values.update(tf_dicts[i3][key])
                            loc_merge_values.update(loc_dicts[i3][key])
                if big_term.__contains__(key):
                    tf_merge_values.update(big_tf_dict[key])
                    loc_merge_values.update(big_loc_dict[key])
                if Parse.isWord(key) and key.isupper():
                    new_key = key.lower()
                    if self.terms_dict.__contains__(new_key):
                        big_term.append(new_key)
                        big_tf_dict[new_key] = tf_merge_values
                        big_loc_dict[new_key] = loc_merge_values
                    else:
                        checked_tf_dict[key] = tf_merge_values
                        checked_loc_dict[key] = loc_merge_values
                else:
                    checked_tf_dict[key] = tf_merge_values
                    checked_loc_dict[key] = loc_merge_values

                '''
                for key in checked_tf_dict:
                    tf_values = checked_tf_dict[key]
                    for doc in tf_values:
                        tf_idf = ((float(tf_values[doc]) / self.docs_indexer[doc].length) *
                                  (math.log10(self.num_of_corpus_docs / float(checked_tf_dict[key].__len__()))))
                        tf_idf_values[doc] = tf_idf
                        if tf_idf > 0.7:
                            self.docs_indexer[doc].num_of_unique_words += 1
                        if tf_values[doc] > self.docs_indexer[doc].max_tf:
                            self.docs_indexer[doc].max_tf = tf_values[doc]
                    checked_tf_idf_dict[key] = tf_idf_values
                    tf_idf_values = {}
                    '''
            for term in big_term:
                if all_terms_to_merge.__contains__(term.upper()) and not checked_tf_dict.__contains__(term):
                    all_terms_to_merge.remove(term.upper())
            self.final_posting(sorted(all_terms_to_merge), checked_tf_dict, checked_loc_dict, False)
            all_terms_from_postings = []
            all_terms_to_merge = []
            checked_tf_dict = {}
            checked_loc_dict = {}
            if self.post_files_blocks[min_ind].__len__() - 1 > read_blocks[min_ind]:
                if num_of_blocks_to_read > self.post_files_blocks[min_ind].__len__() - 1 - read_blocks[min_ind]:
                    num_of_blocks_to_read = self.post_files_blocks[min_ind].__len__() - 1 - read_blocks[min_ind]
                terms[min_ind], tf_dicts[min_ind], loc_dicts[min_ind] = self.read_post_consecutive(
                    min_ind, read_blocks[min_ind], num_of_blocks_to_read)
                read_blocks[min_ind] += num_of_blocks_to_read
                last_min_term = min_term
                min_term = terms[min_ind][terms[min_ind].__len__() - 1]
                # print "posting file: " + str(min_ind) + " num of blocks that was read: " + str(num_of_blocks_to_read)
                num_of_blocks_to_read = 5
            else:
                terms[min_ind] = []
                tf_dicts[min_ind] = {}
                loc_dicts[min_ind] = {}
                last_min_term = min_term
                min_term = "zzzzzzz"
                # num_of_blocks_to_read = 5
        self.post_count += 1

        # Final post file 'post_num' for read is ""

    # Final post file 'post_num' for read is ""
    def final_posting(self, terms, tf_dict, loc_dict, finished):
        # total_size = 0
        compressed_block = None
        self.final_count += len(terms)
        for term in terms:
            freq = 0
            for doc in tf_dict[term]:
                freq += tf_dict[term][doc]
            index = '{}|{}|{}@'.format(term, str(tf_dict[term]), str(loc_dict[term]))
            cur_size = sys.getsizeof(index)
            # compressed_block = zlib.compress(self.block, 4)
            block_size = sys.getsizeof(compressed_block)

            if self.block_size + cur_size < 8192:  # 8192
                self.block = "{}{}".format(self.block, index)
                self.terms_dict[term] = {'block': self.block_count, 'index': self.pos_in_block, "freq": freq}
                self.pos_in_block += 1
                self.block_size += cur_size
            else:
                compressed_block = zlib.compress(self.block, 4)
                self.block_size = sys.getsizeof(compressed_block)
                if self.block_size + cur_size < 8192:  # 8192
                    self.block = "{}{}".format(self.block, index)
                    self.terms_dict[term] = {'block': self.block_count, 'index': self.pos_in_block, "freq": freq}
                    self.pos_in_block += 1
                    self.block_size += cur_size
                else:
                    self.compressed_blocks.append(compressed_block)
                    self.block_count += 1
                    self.block = index
                    self.block_size = cur_size
                    self.terms_dict[term] = [self.block_count, 0]
                    self.pos_in_block = 1

        # if with some size that we'll decide - we want to aggregate many terms before posing
        #   posting
        if self.final_count > 100000 or finished:
            self.final_count = 0
            self.compressed_blocks.append(zlib.compress(self.block, 4))
            self.block = ''
            # self.block_size = 0
            file_name = 'Posting' + str(self.post_count) if not self.to_stem else 'PostingS' + str(self.post_count)
            with open(self.posting_path + file_name, 'ab+') as f:
                for block in self.compressed_blocks:
                    f.write(block)
                    self.post_files_blocks[self.post_count].append(f.tell())
            f.close()
            self.compressed_blocks = []
            self.block_count = 0
            self.pos_in_block = 0
            # self.post_count += 1
            pass

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
        with open("Documents", 'ab+') as f:
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
