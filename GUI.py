import os
from Tkinter import tkinter

from Tkinter import *
import tkFileDialog
import tkMessageBox
from timeit import default_timer as timer

"""
~~~~~~~~~~~~~~~~~~~~~~~~  Module Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Module Contains Methods for creating and managing the Graphic User Interfacs
    of the project 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

"""
   Description :
       This is a generic method for generating tkinter entries 
   Args:
       param1 : Path of the file 
       param2 : The name of the file

   Returns:
       Dictionaries of documents - key = document id , value = Document object
"""


def make_entry(parent, caption, row, column, width=None, **options):
    Label(parent, text=caption).grid(row=row, column=column, sticky='W')
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.grid(row=row, column=column + 1, sticky='W')
    return entry


class View:
    """
       Class Description :
           This Class is used the the gui of the index phase of the search engine
    """

    """
        Description :
            This method is for initializing the indexer properties
    """

    def __init__(self, controller):
        self.controller = controller
        self.stemming_bool = False
        self.with_semantics = False
        self.index_window = Tk()
        self.index_window.protocol("WM_DELETE_WINDOW", self.index_window.destroy)
        self.index_window.title("Documents Inverted Indexing")
        self.corpus_entry = make_entry(self.index_window, "Corpus Path:", 1, 0, 60)
        self.posting_entry = make_entry(self.index_window, "Posting Path:", 2, 0, 60)
        self.language_list = None
        self.currnent_qID = 0

    """
        Description :
            This method is for getting the stemming bool, 
            by the choose of the user in the radio button
    """

    def get_stemming_bool(self):
        return self.stemming_bool

    """
        Description :
            Browse button function - opens file dialog and gets the path of 
            the chosen directiory
    """

    def browse_corpus_dir(self):
        self.corpus_entry.delete(first=0, last=100)
        dir_path = tkFileDialog.askdirectory()
        self.corpus_entry.insert(0, dir_path)
        self.controller.set_corpus_path(dir_path)

    """
        Description :
            Browse button function - opens file dialog and gets the path of 
            the chosen directiory
    """

    def browse_posting_dir(self):
        self.posting_entry.delete(first=0, last=100)
        dir_path = tkFileDialog.askdirectory()
        self.posting_entry.insert(0, dir_path)
        self.controller.set_posting_path(dir_path)

    """
       To be continued..........
    """

    def language_chosen(self):
        pass

    """
         Description :
             reset button function - calls the controller reset function
    """

    def reset(self):
        dir_path = self.posting_entry.get()
        if dir_path == '':
            self.invalid_path("Posting")
            return
        self.controller.set_posting_path(dir_path)
        self.controller.reset()
        self.language_list.insert(END, '')
        tkMessageBox.showinfo('Reset',"Reset Executed Successfully")

    """
         Description :
             start button function - gets paths from entries and calls controller to start the program
    """

    def start(self):
        dir_path = self.corpus_entry.get()
        if not os.path.isdir(dir_path):
            self.invalid_path("Corpus")
            return
        self.controller.set_corpus_path(dir_path)
        dir_path = self.posting_entry.get()
        if not os.path.isdir(dir_path):
            self.invalid_path("Posting")
            return
        self.controller.set_posting_path(dir_path)
        start = timer()
        self.controller.start()
        end = timer()
        tkMessageBox.showinfo('Finished',
                              "Indexed {} docs\nNum of unique terms in the corpus is: {}\nTotal processing time is: {}".format(
                                  len(self.controller.indexer.docs_dict), len(self.controller.indexer.terms_dict),
                                  str(end - start)))
        lang_list = self.controller.get_languages()
        for lang in sorted(lang_list):
            self.language_list.insert(END, lang)

    """
          Description :
              Shows invalid pass message 
    """

    def invalid_path(self, path_type):
        tkMessageBox.showinfo("Error ", "Invalid {} path".format(path_type))

    """
         Description :
             load button function - gets paths from entries and calls controller to start the program
    """

    def load(self):
        dir_path = self.corpus_entry.get()
        if not os.path.isdir(dir_path):
            self.invalid_path("Corpus")
            return
        self.language_list.delete(0, END)
        dir_path = self.posting_entry.get()
        if not os.path.isdir(dir_path):
            self.invalid_path("Posting")
            return
        self.controller.set_posting_path(dir_path)
        self.controller.load()
        lang_list = self.controller.get_languages()
        for lang in sorted(lang_list):
            self.language_list.insert(END, lang)
        tkMessageBox.showinfo('Load',"Loading Executed Successfully")

    """
          Description :
              Show button function - gets terms dictionary from controller and 
              opens a window with box view for the terms and their frequency
    """

    def show(self):
        dict_window = Tk()
        dict_window.geometry("300x900")

        terms_dict = self.controller.get_terms_dict()

        listNodes = Listbox(dict_window, font=("Helvetica", 12))
        listNodes.pack(side="left", fill="y")

        scrollbar = Scrollbar(dict_window, orient="vertical")
        scrollbar.config(command=listNodes.yview)
        scrollbar.pack(side="right", fill="y")

        listNodes.config(yscrollcommand=scrollbar.set)

        for term in sorted(terms_dict.keys()):
            listNodes.insert(END, "{} - {}\n".format(term, str(terms_dict[term][1])))

    """
         Description :
             stem radio button function - gets the user choose from the radio button
    """

    def stem_control(self):
        if self.stemming_bool:
            self.stemming_bool = False
        else:
            self.stemming_bool = True
        self.controller.set_stemming_bool(self.stemming_bool)

    """
          Description :
              Creating the index view window and its buttons
    """

    def start_index_view(self):
        welcome_instruction = Label(master=self.index_window,
                                    text='Hello! In order to proceed, please insert Corpus and Posting paths:')
        welcome_instruction.grid(row=0, column=1)

        browse_corpus = Button(master=self.index_window, text='Browse', width=6, command=self.browse_corpus_dir)
        browse_corpus.grid(row=1, column=2, sticky='W')
        browse_posting = Button(master=self.index_window, text='Browse', width=6, command=self.browse_posting_dir)
        browse_posting.grid(row=2, column=2, sticky='W')

        stemming_check = Checkbutton(master=self.index_window, text="Stemming", command=self.stem_control)
        stemming_check.grid(row=3, column=1, sticky='W')

        start_button = Button(master=self.index_window, text="Start Indexing", command=self.start)
        start_button.grid(row=3, column=1)

        lang_frame = Frame(self.index_window)
        lang_frame.grid(row=5, column=1, sticky='W')

        Label(master=self.index_window, text="Languages:").grid(row=4, column=1, sticky='W')
        self.language_list = Listbox(master=lang_frame, width=20, height=10, command=self.language_chosen())

        scrollbar = Scrollbar(lang_frame, orient="vertical")
        scrollbar.pack(side=RIGHT, fill=Y)

        self.language_list.config(yscrollcommand=scrollbar.set)
        self.language_list.pack(expand=True, fill=Y)
        scrollbar.config(command=self.language_list.yview)

        load_dict_button = Button(master=self.index_window, text="Load Dictionary", command=self.load)
        load_dict_button.grid(row=4, column=1, sticky='E')

        search_Button = Button(master=self.index_window, text="Go To Search",
                               command=self.search_query_file_window)
        search_Button.grid(row=5, column=2)

        show_dict_button = Button(master=self.index_window, text="Show Dictionary", command=self.show)
        show_dict_button.grid(row=4, column=2)
        reset_button = Button(master=self.index_window, text='Reset', width=6, command=self.reset)
        reset_button.grid(row=4, column=3)

        self.index_window.mainloop()

    def search_query_file_window(self):

        def show_entities():
            doc_id = [docs_list.get(idx) for idx in docs_list.curselection()]
            entities = self.controller.get_doc_five_entities(doc_id[0])
            dict_window = Tk()
            dict_window.geometry("300x300")

            list_nodes = Listbox(dict_window, font=("Helvetica", 12))
            list_nodes.pack(side="left", fill="y")

            scrollbar = Scrollbar(dict_window, orient="vertical")
            scrollbar.config(command=list_nodes.yview)
            scrollbar.pack(side="right", fill="y")

            list_nodes.config(yscrollcommand=scrollbar.set)

            for entity in entities:
                list_nodes.insert(END, entity)

        def save():
            dir_path = save_file_results_entry.get()
            if not os.path.isdir(dir_path):
                self.invalid_path("Save")
                self.index_window.lower(search_file_window)
                return
            self.controller.set_save_path(save_file_results_entry.get())
            self.controller.save()
            tkMessageBox.showinfo('Save', "Save Executed Successfully")
            self.index_window.lower(search_file_window)

        def start_query_search():
            query = query_entry.get()
            if query == '' or query is NONE:
                tkMessageBox.showinfo('Query Search', "Query search failed please insert query")
                self.index_window.lower(search_file_window)
                return
            values = set(cities_list.get(idx) for idx in cities_list.curselection())
            docs = self.controller.start_query_search(query_entry.get(), values)
            docs_list.delete(0, END)
            docs_list.insert(END,"Query ID " + str(self.currnent_qID) + " Results:")
            self.currnent_qID += 1
            for doc in docs:
                docs_list.insert(END, doc[0])

        def start_file_search():
            file_path = queries_path_entry.get()
            if not os.path.isfile(file_path):
                self.invalid_path("Queries File")
                self.index_window.lower(search_file_window)
                return
            chosen_cities = [cities_list.get(idx) for idx in cities_list.curselection()]
            queries_results = self.controller.start_file_search(queries_path_entry.get(), chosen_cities)
            docs_list.delete(0, END)
            for query in queries_results:
                docs_list.insert(END, "Query ID " + query[0] + " Results:")
                for doc in query[2]:
                    docs_list.insert(END, doc[0])
                docs_list.insert(END, "")

        def browse_queries_file_dir():
            queries_path_entry.delete(first=0, last=100)
            f = tkFileDialog.askopenfile(parent=search_file_window, mode='rb', title='Choose a file')
            self.index_window.lower(search_file_window)
            queries_path_entry.insert(0, f.name)
            f.close()

        def browse_file_results_save():
            save_file_results_entry.delete(first=0, last=100)
            dir_path = tkFileDialog.askdirectory()
            save_file_results_entry.insert(0, dir_path)

        def on_closing():
            search_file_window.destroy()
            self.index_window.lift()

        def semantics_control():
            if self.with_semantics:
                self.with_semantics = False
            else:
                self.with_semantics = True
            self.controller.set_with_semantics(self.with_semantics)

        cities_names = self.controller.get_cities_list()
        if cities_names is None:
            tkMessageBox.showinfo("Error ", "Please Load Dictionary before Search")
            on_closing()
            return

        search_file_window = Tk()
        self.index_window.lower(search_file_window)
        # search_file_window.geometry("800x600")
        Label(master=search_file_window, text="~~~~~~~~Search With Free Text Query~~~~~~~~").grid(row=0, column=1)
        query_entry = make_entry(search_file_window, "Enter Query:", 1, 0, 60)
        start_button = Button(master=search_file_window, text="Search", command=start_query_search)
        start_button.grid(row=2, column=1)
        search_file_window.protocol("WM_DELETE_WINDOW", on_closing)
        stemming_check = Checkbutton(master=search_file_window, text="Semantics", command=semantics_control)
        stemming_check.grid(row=2, column=1, sticky='W')
        Label(master=search_file_window, text="~~~~~~~~Search With Queries File~~~~~~~~").grid(row=5, column=1)
        queries_path_entry = make_entry(search_file_window, "Queries Path:", 6, 0, 60)
        browse_queries_file = Button(master=search_file_window, text='Browse', width=6,
                                     command=browse_queries_file_dir)
        browse_queries_file.grid(row=6, column=2, sticky='W')
        search_queries_button = Button(master=search_file_window, text="Search", command=start_file_search)
        search_queries_button.grid(row=7, column=1)

        Label(master=search_file_window, text="~~~~~~~~Save Queries Results~~~~~~~").grid(row=8, column=1)
        save_file_results_entry = make_entry(search_file_window, "Save Path:", 9, 0, 60)
        browse_save_file = Button(master=search_file_window, text='Browse', width=6,
                                  command=browse_file_results_save)
        browse_save_file.grid(row=9, column=2, sticky='W')
        save_button = Button(master=search_file_window, text="Save", command=save)
        save_button.grid(row=10, column=1)

        entities_button = Button(master=search_file_window, text="Show Entities", command=show_entities)
        entities_button.grid(row=4, column=1, sticky='E')

        cities_frame = Frame(search_file_window)
        cities_frame.grid(row=4, column=0)

        Label(master=search_file_window, text="Choose Cities:").grid(row=3, column=0, sticky='NW')
        cities_list = Listbox(master=cities_frame, width=20, height=20, selectmode=MULTIPLE)

        cities_scrollbar = Scrollbar(cities_frame, orient="vertical")
        cities_scrollbar.pack(side=RIGHT, fill=Y)

        cities_list.config(yscrollcommand=cities_scrollbar.set)
        cities_list.pack(expand=True, fill=Y)
        cities_scrollbar.config(command=cities_list.yview)

        for city in sorted(cities_names):
            cities_list.insert(END, city)

        docs_frame = Frame(search_file_window)
        docs_frame.grid(row=4, column=1)

        Label(master=search_file_window, text="      Results:").grid(row=4, column=1, sticky='W')
        docs_list = Listbox(master=docs_frame, width=30, height=20)

        docs_scrollbar = Scrollbar(docs_frame, orient="vertical")
        docs_scrollbar.pack(side=RIGHT, fill=Y)

        docs_list.config(yscrollcommand=docs_scrollbar.set)
        docs_list.pack(expand=True, fill=Y)
        docs_scrollbar.config(command=docs_list.yview)

        search_file_window.mainloop()
