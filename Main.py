import os
from GUI import *
# from Indexer import Indexer
from ReadFile import ReadFile
from Parse import Parse
from ReadFile import Document
from timeit import default_timer as timer
from Indexer import Indexer


class Main:

    def __init__(self):
        self.reader = ReadFile()
        self.indexer = Indexer("Postings\\")
        self.parser = Parse()
        self.corpus_path = ''
        self.posting_path = ''
        self.to_stem = False

    def set_corpus_path(self, path):
        self.corpus_path = path

    def set_posting_path(self, path):
        self.posting_path = path

    def set_stemming_bool(self, to_stem):
        self.parser.set_stemming_bool(to_stem)

    def start(self):
        if self.to_stem:
            self.parser.to_stem = True
            self.indexer.to_stem = True
        mstart = timer()
        self.set_corpus_path(os.path.dirname(os.path.abspath(__file__)) + "\\corpus")
        #self.indexer.posting_path = self.posting_path
        print "start"
        doc_terms_dict = {}
        locs_dict = {}
        dirs_list = os.listdir(self.corpus_path)
        i = 0
        j = 0
        file_docs = {}
        docs = {}
        num_of_docs = 0
        terms = 0
        while i < len(dirs_list):
            # while i < 1:
            docs = self.reader.separate_docs_in_file(self.corpus_path, dirs_list[i])
            # file_docs[dirs_list[i]] = docs.keys()
            j = 0
            # self.indexer.files_count += 1
            # for doc_id in docs:
            #     self.parser.parsed_doc = docs[doc_id]
            #     doc_terms_dict = self.parser.main_parser(docs[doc_id].text)
                # print docs[doc_id].length
                # print docs[doc_id].num_of_unique_words
                # print docs[doc_id].max_tf
                # num_of_docs+=1
                # terms+=len(doc_dict)
                # if i == len(dirs_list) - 1 and j == len(docs) - 1:
                #     self.indexer.finished_parse = True
                # self.indexer.index_terms(doc_terms_dict, doc_id)
                # j += 1
                # docs[doc_id].text = None
            i += 1
        print(len(self.reader.cities))
        # self.indexer.read_post(0, [0, 1, 2])
        # self.indexer.finished_parse = True
        # mend = timer()
        # print("total Index time: " + str(mend - mstart))
        # self.indexer.merge_posting()
        # self.indexer.non_compressed_post()
        # self.indexer.index_cities(self.reader.cities)
        # self.indexer.read_post("", "")
        # print terms
        # print num_of_docs

    def load(self):
        self.indexer.load()
        pass

    def reset(self):
        for the_file in os.listdir(self.posting_path):
            file_path = os.path.join(self.posting_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        self.indexer = Indexer()
        self.reader = ReadFile()
        self.parser = Parse()

    def get_terms_dict(self):
        # return  terms-dfs
        pass

    def get_languages(self):
        # should return string with languages separated with '\n'
        return self.reader.languages


start = timer()
main = Main()
# view = IndexView(main)
# view.start_index_view()
# main.to_stem = view.get_stemming_bool()
main.start()
end = timer()
print("total time: " + str(end - start))

'''''
parse = Parse()
parse.main_parser(" ")
'''''
