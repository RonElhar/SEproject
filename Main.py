import os

import shutil

import Merge
from GUI import *
# from Indexer import Indexer
from ReadFile import ReadFile
from Parse import Parse
from ReadFile import Document
from timeit import default_timer as timer
from Indexer import Indexer
import ParallelMain
import datetime
import Parse


class Main:
    def __init__(self):
        self.corpus_path = ''
        self.posting_path = ''
        self.to_stem = False
        self.indexer = None
        self.reader = ReadFile()
        self.languages = set()

    def set_corpus_path(self, path):
        self.corpus_path = path

    def set_posting_path(self, path):
        self.posting_path = path

    def set_stemming_bool(self, to_stem):
        self.to_stem = to_stem

    def start(self):
        if not os.path.exists(self.posting_path):
            os.makedirs(self.posting_path)
        self.indexer = Indexer(self.posting_path)
        if self.to_stem:
            self.indexer.to_stem = True
        start_time = timer()
        print "start :" + str(datetime.datetime.now())
        dirs_list = os.listdir(self.corpus_path)
        # ''''
        dirs_dict = ParallelMain.start(self.corpus_path, self.posting_path, self.to_stem, dirs_list)
        print "finished_postings: " + str(datetime.datetime.now())
        docs = {}
        # '''
        i = 0
        # while i < len(dirs_list):
        while i < 40:
            self.reader.read_cities(self.corpus_path, dirs_list[i])
            i += 1
        files_names = []
        post_files_lines = []
        for dir in dirs_dict.keys():
            docs.update(dirs_dict[dir][2])
            for lang in dirs_dict[dir][3]:
                self.languages.add(lang)
            old_post_files_lines = dirs_dict[dir][0]
            for i in range(0, len(old_post_files_lines)):
                files_names.append(dir + "\\Posting" + str(i) if not self.to_stem else dir + "\\sPosting" + str(i))
                post_files_lines.append(old_post_files_lines[i])

        print "started merge: " + str(datetime.datetime.now())

        terms_dicts = [dirs_dict["\\Postings1"][1], dirs_dict["\\Postings2"][1], dirs_dict["\\Postings3"][1],
                       dirs_dict["\\Postings4"][1]]

        terms_dict = Merge.start_merge(files_names, post_files_lines, terms_dicts, self.posting_path, self.to_stem)
        print "finished merge: " + str(datetime.datetime.now())

        dirs_dict = None
        self.indexer.terms_dict = terms_dict
        self.indexer.index_docs(docs)
        self.indexer.index_cities(self.reader.cities)
        self.indexer.post_pointers(self.languages)
        end_time = timer()

        print("total time: " + str(end_time - start_time))
        print "End: " + str(datetime.datetime.now())

        self.report()

    def load(self):
        self.indexer = Indexer(self.posting_path)
        self.languages = self.indexer.load()
        pass

    def reset(self):
        shutil.rmtree(self.posting_path)
        if not os.path.exists(self.posting_path):
            os.makedirs(self.posting_path)
        self.indexer = None

    def get_terms_dict(self):
        return self.indexer.terms_dict

    def get_languages(self):
        # should return string with languages separated with '\n'
        return self.languages

    def report(self):
        print "Num of terms: " + str(len(self.indexer.terms_dict))
        num_count = 0
        i = 0
        print "Num of terms which are nums: " + str(num_count)
        print "Num of countries: " + str(len(self.indexer.countries))
        print "Num of capitals: " + str(self.indexer.num_of_capitals)


if __name__ == "__main__":
    controller = Main()
    view = IndexView(controller)
    view.start_index_view()

'''''
parse = Parse()
parse.main_parser(" ")
'''''
