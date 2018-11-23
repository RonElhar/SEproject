import os
import GUI
# from Indexer import Indexer
from ReadFile import ReadFile
from Parse import Parse
from ReadFile import Document
from timeit import default_timer as timer
from Indexer import Indexer


class Main:
    def __init__(self):
        self.reader = ReadFile()
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\corpus"
        self.parser = Parse()
        self.indexer = Indexer("Postings\\")

    def start(self):
        doc_dict = {}
        locs_dict = {}
        dirs_list = os.listdir(self.ROOT_DIR)
        i = 0
        file_docs = {}
        docs = {}
        num_of_docs = 0
        terms = 0
        #while i < len(dirs_list):
        #while i < 10:
        self.indexer.docs_indexer = self.reader.separate_docs_in_file(self.ROOT_DIR, "FB396001")
            # num_of_docs += self.indexer.docs_indexer.__len__()
            # file_docs[dirs_list[i]] = docs.keys()
            #i += 1
            #self.indexer.files_count += 1

        # for filename in :
            #   docs = self.reader.separate_docs_in_file(self.ROOT_DIR, filename)
            # docs = self.reader.separate_docs_in_file(self.ROOT_DIR, "FB396001")
        for doc_id in self.indexer.docs_indexer:
            num_of_docs += 1
            # print(doc.id)
            doc_dict = self.parser.main_parser(self.indexer.docs_indexer[doc_id].text)
            self.indexer.docs_indexer[doc_id].text = None
            self.indexer.docs_indexer[doc_id].length = doc_dict.__len__()
            self.indexer.index_terms(doc_dict, doc_id)

        #self.indexer.read_post(0, [0, 1, 2])
        # self.indexer.merge_posting()
        # print num_of_docs


start = timer()
main = Main()
main.start()
end = timer()
print("total time: " + str(end - start))
'''''
parse = Parse()
parse.main_parser(" ")
'''''
