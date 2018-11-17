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
        docs_dict = {}
        #for filename in os.listdir(self.ROOT_DIR):
        #docs = self.reader.separate_docs_in_file(self.ROOT_DIR, filename)
        docs = {}
        docs = self.reader.separate_docs_in_file(self.ROOT_DIR, "FB396001")
        d_c = 0
        for doc in docs:
            #print(doc.id)
            docs_dict[doc] = self.parser.main_parser(docs[d_c].text)
            d_c += 1
        #self.indexer.index_terms(docs_dict, docs)
     #   print "numbers time: " + str (self.parser.number_terms_time)
     #   print "getTerms time: " + str(self.parser.get_terms_time)
     #   print "rangeTerms time " + str(self.parser.range_term_time)
      #  print "uniteDicts time: " + str(self.parser.unite_dicts_time)
      #  print "total parse time: " + str(self.parser.main_parser_time)

parse = Parse()
parse.main_parser(["world", "6-7", "1000-2000", "Aviad", "Between", "6000", "and", "7000", "World", "May", "1994", "14",
                   "MAY", "JUNE", "4", "20.6bn", "Dollars", "32bn", "Dollars", "Aviad", "$100", "million", "40.5",
                   "Dollars", "100", "billion", "U.S.", "dollars", "NBA", "320", "million", "U.S.", "dollars", "1",
                   "trillion", "U.S.", "dollars", "22 3/4", "Dollars", "NBA", "$100", "billion"])

#start = timer()
#main = Main()
#main.start()
#end = timer()
#print("total time: " + str(end-start))