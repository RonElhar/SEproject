import os
from GUI import *
# from Indexer import Indexer
from ReadFile import ReadFile
from Parse import Parse
from ReadFile import Document
from timeit import default_timer as timer
from Indexer import Indexer
from multiprocessing import Pool


def parse_docs(document):
    parser = Parse()
    document_dict = parser.main_parser(document.text)
    document.text = None
    return document_dict


if __name__ == "__main__":
    dirs_list = os.listdir("C:\\Users\\USER\\Desktop\\SearchEngine\\corpus")
    docs = {}
    start = timer()
    p = Pool()
    reader = ReadFile()
    indexer = Indexer("C:\\Users\\USER\\Desktop\\SearchEngine\\Postings")
    for dir in dirs_list:
        docs = reader.separate_docs_in_file("C:\\Users\\USER\\Desktop\\SearchEngine\\corpus", dirs_list[0])
        docs_dict = p.map(parse_docs, docs.values())
#        indexer.parallel_index_terms(docs_dict, docs.keys())
    end = timer()
    print("total time: " + str(end - start))

# view = IndexView(main)
# view.start_index_view()
# main.start()
