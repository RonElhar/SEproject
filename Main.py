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

    def set_corpus_path(self, path):
        self.corpus_path = path

    def set_posting_path(self, path):
        self.posting_path = path

    def set_stemming_bool(self, to_stem):
        self.parser.set_stemming_bool(to_stem)

    def start(self):
        self.set_corpus_path(os.path.dirname(os.path.abspath(__file__)) + "\\corpus")
        doc_dict = {}
        locs_dict = {}
        dirs_list = os.listdir(self.corpus_path)
        i = 0
        file_docs = {}
        docs = {}
        num_of_docs = 0
        terms = 0
        while i < len(dirs_list):
        # while i < 10:
            docs = self.reader.separate_docs_in_file(self.corpus_path, dirs_list[i])
            # file_docs[dirs_list[i]] = docs.keys()
            i += 1
            #self.indexer.files_count += 1
            for doc_id in docs:
                # print(doc.id)
                doc_dict = self.parser.main_parser(docs[doc_id].text)
                # num_of_docs+=1
                # terms+=len(doc_dict)
                self.indexer.index_terms(doc_dict, doc_id)
                docs[doc_id].text = None
        #self.indexer.read_post(0, [0, 1, 2])
        # self.indexer.merge_posting()
        #self.indexer.index_cities(self.reader.cities)
        # self.indexer.read_post("", "")
        # print terms
        # print num_of_docs

    def load(self):
        for the_file in os.listdir(self.posting_path):
            file_path = os.path.join(self.posting_path, the_file)
            try:
                pass
            # load Postings files
            except Exception as e:
                print(e)
        pass

    def reset(self):
        for the_file in os.listdir(self.posting_path):
            file_path = os.path.join(self.posting_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

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
main.start()
end = timer()
print("total time: " + str(end - start))

'''''
parse = Parse()
parse.main_parser(" ")
'''''
