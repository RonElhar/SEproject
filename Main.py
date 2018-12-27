import linecache

from GUI import View
from operator import itemgetter
from ReadFile import ReadFile
from Parse import Parse
from Indexer import Indexer
import shutil
import Merge
import os
import ParallelMain
import Parse
from Searcher import Searcher
from gensim.models import Word2Vec

"""
~~~~~~~~~~~~~~~~~~~~~~~~  Module Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Module runs the whole program,
    It contains the Main class which is the Controller of the MVC model for
    Event Driven Programming, and a script which starts the project
    
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class Main:
    """
        Class Description :
            Implements the Controller of the MVC model, runs the project.
    """

    """
        Desctiption
            This method is for initializing Main's properties
    """

    def __init__(self):
        self.main_path = ''
        self.posting_path = ''
        self.to_stem = False
        self.indexer = None
        self.reader = ReadFile()
        self.languages = set()
        self.searcher = None
        self.queries_docs_results = []
        self.avg_doc_length = 0
        self.with_semantics = False
        self.with_stem = False
        self.save_path = ''

    """
        Description :
            This method manages the program 
    """

    def start(self):
        self.indexer = Indexer(self.posting_path)
        if self.to_stem:
            self.indexer.to_stem = True
        dirs_list = os.listdir(self.main_path + '\\corpus')
        # Create temp postings Multiprocessing
        dirs_dict = ParallelMain.start(self.main_path, self.posting_path, self.to_stem, dirs_list)
        # Merging dictionaries that were created by the processes
        docs = {}
        files_names = []
        post_files_lines = []
        total_length = 0
        for dir in dirs_dict.keys():
            tmp_docs_dict = dirs_dict[dir][2]
            for doc_id in tmp_docs_dict:
                docs[doc_id] = tmp_docs_dict[doc_id]
                total_length += docs[doc_id].length
            for lang in dirs_dict[dir][3]:
                self.languages.add(lang)
            old_post_files_lines = dirs_dict[dir][0]
            for i in range(0, len(old_post_files_lines)):
                files_names.append(dir + "\\Posting" + str(i) if not self.to_stem else dir + "\\sPosting" + str(i))
                post_files_lines.append(old_post_files_lines[i])

        self.avg_doc_length = total_length / len(docs)

        # Gets Cities that appear in the corpus
        i = 0
        while i < len(dirs_list):
            self.reader.read_cities(self.main_path + '\\corpus', dirs_list[i])
            i += 1

        terms_dicts = [dirs_dict["\\Postings1"][1], dirs_dict["\\Postings2"][1], dirs_dict["\\Postings3"][1],
                       dirs_dict["\\Postings4"][1]]

        terms_dict = Merge.start_merge(files_names, post_files_lines, terms_dicts, self.posting_path, self.to_stem)

        self.indexer.docs_avg_length = self.avg_doc_length
        self.indexer.terms_dict = terms_dict
        self.indexer.docs_dict = docs
        self.indexer.index_cities(self.reader.cities)
        self.indexer.post_pointers(self.languages)
        # self.searcher = Searcher(self.main_path, self.posting_path, self.indexer.terms_dict, self.indexer.cities_dict,
        #                          self.indexer.docs_dict, self.avg_doc_length, self.to_stem, self.with_semantics)
        # self.searcher.model = Word2Vec.load('model.bin')
        # path = self.posting_path + '\FinalPost' + '\Final_Post'
        # linecache.getline(path, 500000)

    """
        Description :
            This method calls the Indexer function for loading saved files to the programs main memory
    """

    def load(self):

        self.indexer = Indexer(self.posting_path)
        if self.to_stem:
            self.indexer.to_stem = True
        self.languages = self.indexer.load()
        self.avg_doc_length = self.indexer.docs_avg_length
        self.searcher = Searcher(self.main_path, self.posting_path, self.indexer.terms_dict, self.indexer.cities_dict,
                                 self.indexer.docs_dict, self.avg_doc_length, self.to_stem, self.with_semantics)
        self.searcher.model = Word2Vec.load('model.bin')

    # self.searcher.search("china is great", {})

    """
        Description :
            This method erases all of the files in the Posting path
    """

    def reset(self):
        shutil.rmtree(self.posting_path)
        if not os.path.exists(self.posting_path):
            os.makedirs(self.posting_path)
        self.indexer = None

    """
        Description :
            This method returns the terms dictionary, used by GUI IndexView for showing the dictionary.
    """

    def get_terms_dict(self):
        return self.indexer.terms_dict

    """
        Description :
            This method returns the Languages of the corpus, used by GUI IndexView for showing the lagnuages.
    """

    def get_languages(self):
        # should return string with languages separated with '\n'
        return self.languages

    """
        Description  :
            This method gets the corpus path from the GUI
    """

    def set_corpus_path(self, path):
        self.main_path = path

    """
         Description  :
             This method gets the posting path from the GUI
    """

    def set_posting_path(self, path):
        self.posting_path = path

    """
         Description  :
             This method gets the stemming bool from the GUI
    """

    def set_stemming_bool(self, to_stem):
        self.to_stem = to_stem

    def set_with_semantics(self, with_semantics):
        self.with_semantics = with_semantics

    def report(self):
        num_count = 0
        i = 0
        freq = {}
        for term in self.indexer.terms_dict.keys():
            if Parse.isFloat(term):
                num_count += 1
            freq[term] = self.indexer.terms_dict[term][1]

        freq_list = sorted(freq.items(), key=itemgetter(1))
        with open('frequency.txt', 'wb') as f:
            for n in freq_list:
                f.write(str(n[0]) + ": " + str(n[1]) + '\n')

        print "Num of terms which are nums: " + str(num_count)
        print "Num of countries: " + str(len(self.indexer.countries))
        print "Num of capitals: " + str(self.indexer.num_of_capitals)

    def set_save_path(self, dir_path):
        self.save_path = dir_path

    def save(self):
        file_name = ''
        if self.to_stem:
            file_name += 's'
        if self.with_semantics:
            file_name += 's'
        file_name = '\\' + file_name + 'results.txt'
        with open(self.save_path + file_name, 'a+') as f:
            for query_result in self.queries_docs_results:
                for doc in query_result[2]:
                    line = " {} 0 {} 1 42.38 {}\n".format(query_result[0], doc[0], 'rg')
                    f.write(line)
        with open(self.save_path + "\\results4u", 'a+') as f:
            for query_result in self.queries_docs_results:
                f.write("Results For {}\n".format(query_result[0]))
                for doc in query_result[2]:
                    line = " {} \n".format(doc[0])
                    f.write(line)

    def get_cities_list(self):
        if self.indexer is None:
            return None
        return self.indexer.cities_dict.keys()

    def start_query_search(self, query, chosen_cities):
        return self.searcher.search(query, chosen_cities)

    def start_file_search(self, queries_path_entry, chosen_cities):
        queries_list = []
        current_queries_results = []
        with open(queries_path_entry, 'rb') as f:
            lines = f.readlines()
            id = 0
            for line in lines:
                if '<num>' in line:
                    id = line.split(':')[1].replace('\n', '')
                elif '<title>' in line:
                    query = line.replace('<title>', '').replace('\n', '')
                    queries_list.append((id, query))
                    ### option add desc or narr
        for query_tuple in queries_list:
            docs_result = self.start_query_search(query_tuple[1], chosen_cities)
            tmp = (query_tuple[0], query_tuple[1], docs_result)
            current_queries_results.append(tmp)
            self.queries_docs_results.append(tmp)

        return self.queries_docs_results

    def get_doc_five_entities(self, doc_id):
        return self.searcher.docs_dict[doc_id].five_entities


"""
Script Description:
    This script starts the program by initializing Main object, GUI IndexView object
    and calling a function to open the index window.
"""

if __name__ == "__main__":
    controller = Main()
    view = View(controller)
    view.start_index_view()
