import os


from Indexer import Indexer
from ReadFile import ReadFile
from Parse import Parse
from ReadFile import Document
from timeit import default_timer as timer

class Main:
    def __init__(self):
        self.reader = ReadFile()
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "\\corpus"
        self.parser = Parse()
        self.indexer = Indexer("posting path")

    def start(self):
        doc_dict = {}
        locs_dict = {}
        #for filename in os.listdir(self.ROOT_DIR):
        #docs = self.reader.separate_docs_in_file(self.ROOT_DIR, filename)
        docs = self.reader.separate_docs_in_file(self.ROOT_DIR, "FB396001")
        d_c = 0
        for doc in docs:
            #print(doc.id)
            doc_dict[doc.id] = self.parser.main_parser(docs[d_c].text)
            self.indexer.index_terms(doc_dict, doc)
            docs[d_c].text = ''
            d_c += 1


start = timer()
main = Main()
main.start()
end = timer()
print("total time: " + str(end-start))
'''''
parse = Parse()
parse.main_parser(" ")
'''''