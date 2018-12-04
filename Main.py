import os

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


class Main:
    def __init__(self):
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
        self.indexer = Indexer(self.posting_path)
        if self.to_stem:
            self.indexer.to_stem = True
        start_time = timer()
        print "start"
        dirs_dict = ParallelMain.start(self.corpus_path, self.posting_path, self.to_stem)
        print "finished_postings :" + str(datetime.datetime.now())
        files_names = []
        languages = set()
        cities = {}
        docs = {}
        terms_dict = {}
        post_files_lines = []
        #post_files_lines, files_names, cities, docs, languages = Merge.posting_dicts_merge(dirs_dict, self.to_stem)

        for dir in dirs_dict.keys():

            docs.update(dirs_dict[dir][4])

            for language in dirs_dict[dir][3]:
                languages.add(language)

            for city in dirs_dict[dir][2]:
                if city in cities:
                    cities[city].extend(dirs_dict[dir][2][city])
                else:
                    cities[city] = dirs_dict[dir][2][city]

            old_post_files_lines = dirs_dict[dir][0]
            for i in range(0, len(old_post_files_lines)):
                files_names.append(dir + "\\Posting" + str(i) if not self.to_stem else dir + "\\PostingS" + str(i))
                post_files_lines.append(old_post_files_lines[i])

        # for dir in dirs_dict.keys():
        #     for i in range(0, len(dirs_dict[dir])):
        #         if not i == 1:
        #             dirs_dict[dir][i] = None

        print "started merge: " + str(datetime.datetime.now())
        terms_dict = Merge.start_merge(files_names, post_files_lines,
                                       [dirs_dict["\\Postings1"][1], dirs_dict["\\Postings2"][1],
                                        dirs_dict["\\Postings3"][1], dirs_dict["\\Postings4"][1]], self.posting_path,
                                       self.to_stem)
        dirs_dict = None
        self.indexer.terms_dict = terms_dict

        end_time = timer()
        print("total time: " + str(end_time - start_time))
        print "End: " + str(datetime.datetime.now())
        pass

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
        return self.indexer.terms_dict

    def get_languages(self):
        # should return string with languages separated with '\n'
        return self.reader.languages


if __name__ == "__main__":
    controller = Main()
    view = IndexView(controller)
    view.start_index_view()

'''''
parse = Parse()
parse.main_parser(" ")
'''''
