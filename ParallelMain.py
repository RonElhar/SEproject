import os
from ReadFile import ReadFile
from Parse import Parse
from Indexer import Indexer
import multiprocessing

"""
~~~~~~~~~~~~~~~~~~~~~~~~  Module Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Module contains methods for performing MultiProcessed creation of temp posting files
    It divides the given corpus to 4 parts by size and creates 4 processes, one for each quarter.
    Each process creates temp posting files for its part of corpus 
    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


def start_indexing(dirs_list, dirs_dicts, main_path, posting_path, to_stem, start_index, end_index,
                   directory):
    dirs_dicts[directory] = None
    reader = ReadFile()
    parser = Parse(main_path)
    indexer = Indexer(posting_path + directory)

    if to_stem:
        parser.to_stem = True
        indexer.to_stem = True
    if not os.path.exists(posting_path + directory):
        os.makedirs(posting_path + directory)

    documents = {}
    i = start_index
    while i < end_index:
        docs = reader.separate_docs_in_file(main_path + '\\corpus', dirs_list[i])
        j = 0
        for doc_id in docs:
            parser.parsed_doc = docs[doc_id]
            doc_dict = parser.main_parser(docs[doc_id].text)
            docs[doc_id].text = None
            if i == end_index - 1 and j == len(docs) - 1:
                indexer.finished_parse = True
            indexer.index_terms(doc_dict, doc_id)
            documents[doc_id] = docs[doc_id]
            j += 1
        i += 1
    dirs_dicts[directory] = [indexer.post_files_lines, indexer.terms_dict, documents, reader.languages]


"""
    Description :
        This method finds the 4 partition indexes of the corpus by the size of the files 
    Args:
        param1 : List of directories names
        param2 : Corpus path given by user
    Returns:
        List of files indexes which are the partition of the corpus to 4
"""


def get_corpus_4partition(dirs_list, main_path):
    files_partition = []

    def get_size(start_path):
        total_size = 0
        for dir_path, dir_names, file_names in os.walk(start_path):
            for f in file_names:
                fp = os.path.join(dir_path, f)
                total_size += os.path.getsize(fp)
        return total_size

    corpus_size = get_size(main_path)
    process_size = corpus_size / 4
    cur_size = 0
    i = 0
    for directory in dirs_list:
        dir_size = get_size(main_path + '\\' + directory)
        if dir_size + cur_size > process_size:
            files_partition.append(i)
            cur_size = 0
        else:
            cur_size += dir_size
        i += 1

    return files_partition


"""
    Description :
        This method creates 4 processes that perform the creation of the temp posting files
    Args:
        param1 : Corpus path given by user
        param2 : Posting path given by user
        param3 : Stemming bool
        param4 : List of directories names
    Returns:
        Dictionary of dictionaries that where created by the processes
"""


def start(main_path, posting_path, to_stem, dirs_list):
    files_partition = get_corpus_4partition(dirs_list, main_path + '\\corpus')
    manager = multiprocessing.Manager()
    dirs_dicts = manager.dict()

    p1 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, main_path, posting_path, to_stem, 0, files_partition[0],
                                     "\\Postings1"))

    p2 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, main_path, posting_path, to_stem, files_partition[0],
                                     files_partition[1],
                                     "\\Postings2"))

    p3 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, main_path, posting_path, to_stem, files_partition[1],
                                     files_partition[2],
                                     "\\Postings3"))

    p4 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, main_path, posting_path, to_stem, files_partition[2],
                                     len(dirs_list), "\\Postings4"))
    """
    p1 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, main_path, posting_path, to_stem, 0, 2,
                                     "\\Postings1"))

    p2 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, main_path, posting_path, to_stem, 2,
                                     4,
                                     "\\Postings2"))

    p3 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, main_path, posting_path, to_stem, 4,
                                     8,
                                     "\\Postings3"))

    p4 = multiprocessing.Process(target=start_indexing,
                                 args=(
                                     dirs_list, dirs_dicts, main_path, posting_path, to_stem, 8,
                                     10, "\\Postings4"))
   """

    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    return dirs_dicts
