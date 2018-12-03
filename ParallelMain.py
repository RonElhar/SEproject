import os
from GUI import *
from ReadFile import ReadFile
from Parse import Parse
from timeit import default_timer as timer
from Indexer import Indexer
import multiprocessing


def start_indexing(dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, start_index, end_index, directory):
    reader = ReadFile()
    parser = Parse()
    indexer = Indexer(posting_path + directory)
    documents = {}
    if to_stem:
        parser.to_stem = True
        indexer.to_stem = True
    if not os.path.exists(posting_path + directory):
        os.makedirs(posting_path + directory)
    i = start_index
    while i < end_index:
        docs = reader.separate_docs_in_file(corpus_path, dirs_list[i])
        j = 0
        for doc_id in docs:
            parser.parsed_doc = docs[doc_id]
            doc_dict = parser.main_parser(docs[doc_id].text)
            docs[doc_id] = None
            if i == end_index - 1 and j == len(docs) - 1:
                indexer.finished_parse = True
            indexer.index_terms(doc_dict, doc_id)
            documents[doc_id] = docs[doc_id]
            j += 1
        i += 1
    indexer.merge_posting()
    dirs_dicts[directory] = [indexer.post_files_blocks, indexer.terms_dict, reader.cities, reader.languages , documents]


def start(corpus_path, posting_path, to_stem):
    dirs_list = os.listdir(corpus_path)
    manager = multiprocessing.Manager()
    dirs_dicts = manager.dict()
    start_time = timer()
    p1 = multiprocessing.Process(target=start_indexing,
                                 args=(dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 0, 440, "\\Postings1"))
    p1.start()
    p2 = multiprocessing.Process(target=start_indexing,
                 args=(dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 440, 820, "\\Postings2"))
    p2.start()
    p3 = multiprocessing.Process(target=start_indexing,
                 args=(dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 820, 1300, "\\Postings3"))
    p3.start()
    p4 = multiprocessing.Process(target=start_indexing,
                 args=(dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 1300, 1815, "\\Postings4"))
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    end_time = timer()
    print("total time: " + str(end_time - start_time))
    return dirs_dicts
