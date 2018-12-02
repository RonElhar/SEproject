import os
from GUI import *
# from Indexer import Indexer
from ReadFile import ReadFile
from Parse import Parse
from ReadFile import Document
from timeit import default_timer as timer
from Indexer import Indexer
import ParallelMain


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
        indexer = Indexer("\\Postings")
        if self.to_stem:
             indexer.to_stem = True
        start_time = timer()

        consecutive_post_files = {}
        post_file_blocks = []
        print "start"
        dirs_dict = ParallelMain.start(self.corpus_path, self.posting_path, self.to_stem)
        languages = set()
        cities = {}
        docs = {}
        terms = {}
        for dir in dirs_dict.keys():
            docs.update(dirs_dict[dir][4])
        for dir in dirs_dict.keys():
            dirs_dict[dir][4] = None
        for dir in dirs_dict.keys():
            for language in dirs_dict[dir][3]:
                languages.add(language)
        for dir in dirs_dict.keys():
            dirs_dict[dir][3] = None
        for dir in dirs_dict.keys():
            for city in dirs_dict[dir][2]:
                if city in cities:
                    cities[city].extend(docs)
                else:
                    cities[city] = dirs_dict[dir][2][city]
        for dir in dirs_dict.keys():
            dirs_dict[dir][2] = None
        for dir in dirs_dict.keys():
            terms.update(dirs_dict[dir][1])
        for dir in dirs_dict.keys():
            dirs_dict[dir][1] = None
        j = 0
        for dir in dirs_dict.keys():
            old_post_files_block = dirs_dict[dir][0]
            for i in range(0, len(old_post_files_block)):
                consecutive_post_files[j] = dir + "\\Posting" + str(i) if not self.to_stem else dir + "\\PostingS" + str(i)
                post_file_blocks.append(old_post_files_block[i])
                j += 1
        dirs_dict = None
        indexer.post_files_blocks = post_file_blocks
        indexer.consecutive_post_files = consecutive_post_files
        post_file_blocks = None
        consecutive_post_files = None
        indexer.terms_dict = terms
        indexer.merge_posting()
        end_time = timer()
        print("total time: " + str(end_time - start_time))
        print "End"
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
