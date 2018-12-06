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


class IndexView:
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
        self.index_window = Tk()
        self.index_window.title("Documents Inverted Indexing")
        self.corpus_entry = make_entry(self.index_window, "Corpus Path:", 1, 0, 60)
        self.posting_entry = make_entry(self.index_window, "Posting Path:", 2, 0, 60)
        self.language_list = None
        self.start_index_view()

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
        self.controller.set_posting_path(dir_path)
        self.controller.reset()
        self.language_list.insert(END, '')
        pass

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
        show_dict_button = Button(master=self.index_window, text="Show Dictionary", command=self.show)
        show_dict_button.grid(row=4, column=2)
        reset_button = Button(master=self.index_window, text='Reset', width=6, command=self.reset)
        reset_button.grid(row=4, column=3)

        self.index_window.mainloop()
