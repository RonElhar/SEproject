import os
from GUI import *
from ReadFile import ReadFile
from Parse import Parse
from timeit import default_timer as timer
from Indexer import Indexer
import multiprocessing

import sys


def start_indexing(dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, start_index, end_index,
                   directory):
    dirs_dicts[directory] = None
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
    documents = {}
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
    dirs_dicts[directory] = [indexer.post_files_lines, indexer.terms_dict, documents, reader.languages]


def get_corpus_4partition(dirs_list, corpus_path):
    files_partition = []

    def get_size(start_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    corpus_size = get_size(corpus_path)
    process_size = corpus_size / 4
    cursize = 0
    i = 0
    for directory in dirs_list:
        dir_size = get_size(corpus_path + '\\' + directory)
        if dir_size + cursize > process_size:
            files_partition.append(i)
            cursize = 0
        else:
            cursize += dir_size
        i += 1

    return files_partition


def start(corpus_path, posting_path, to_stem, dirs_list):
    files_partition = get_corpus_4partition(dirs_list, corpus_path)
    manager = multiprocessing.Manager()
    dirs_dicts = manager.dict()
    start_time = timer()
    dirs_names = ["\\Postings1", "\\Postings2", "\\Postings3", "\\Postings3"]
    p1 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 0, files_partition[0],
                                     "\\Postings1"))  # 0-395

    p2 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, files_partition[0],
                                     files_partition[1],
                                     "\\Postings2"))  # 395-791

    p3 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, files_partition[1],
                                     files_partition[2],
                                     "\\Postings3"))  # 791, 1243

    p4 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, files_partition[2],
                                     len(dirs_list), "\\Postings4"))


    # p1 = multiprocessing.Process(target=start_indexing,
    #                              args=(
    #                                  dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 0, 10,
    #                                  "\\Postings1"))  # 0-395
    # p2 = multiprocessing.Process(target=start_indexing,
    #                              args=(
    #                                  dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 10,
    #                                  20, "\\Postings2"))  # 395-791
    # p3 = multiprocessing.Process(target=start_indexing,
    #                              args=(
    #                                  dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 20,
    #                                  30, "\\Postings3"))  # 791, 1243
    #
    p4 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, corpus_path, posting_path, to_stem, 30, 40,
                                     "\\Postings4"))  # 1243, 1815

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()
    end_time = timer()
    print("total time: " + str(end_time - start_time))
    return dirs_dicts
