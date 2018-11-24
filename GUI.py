from Tkinter import tkinter

from Tkinter import *
import tkFileDialog


def make_entry(parent, caption, row, column, width=None, **options):
    Label(parent, text=caption).grid(row=row, column=column, sticky='W')
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.grid(row=row, column=column + 1, sticky='W')
    return entry


class IndexView:
    def __init__(self, controller):
        self.controller = controller
        self.stemming_bool = False
        self.index_window = Tk()
        self.index_window.title("Documents Inverted Indexing")
        # self.index_window.config(bg="LightBlue")
        self.corpus_entry = make_entry(self.index_window, "Corpus Path:", 1, 0, 60)
        self.posting_entry = make_entry(self.index_window, "Posting Path:", 2, 0, 60)
        self.language_list = None

    def get_stemming_bool(self):
        return self.stemming_bool

    def browse_corpus_dir(self):
        dir_path = tkFileDialog.askdirectory()
        self.corpus_entry.insert(0, dir_path)
        self.controller.set_corpus_path(dir_path)

    def entered_posting(self):
        dir_path = self.posting_entry.get()
        self.controller.set_posting_path(dir_path)

    def language_chosen(self):
        pass

    def reset(self):
        self.controller.reset()
        self.language_list.insert(END, '')
        pass

    def start(self):
        dir_path = tkFileDialog.askdirectory()
        self.posting_entry.insert(0, dir_path)
        self.controller.set_posting_path(dir_path)
        dir_path = self.corpus_entry.get()
        self.controller.set_corpus_path(dir_path)
        self.controller.start()

        lang_list = self.controller.get_languages()
        for lang in sorted(lang_list):
            self.language_list.insert(END, lang)

    def load(self):
        self.controller.load()
        lang_list = self.controller.get_languages()
        for lang in sorted(lang_list):
            self.language_list.insert(END, lang)

    def show(self):
        dict_window = Tk()
        dict_window.geometry("200x500")
        # dict = self.controller.get_terms_dict()

        listNodes = Listbox(dict_window, font=("Helvetica", 12))
        listNodes.pack(side="left", fill="y")

        scrollbar = Scrollbar(dict_window, orient="vertical")
        scrollbar.config(command=listNodes.yview)
        scrollbar.pack(side="right", fill="y")

        listNodes.config(yscrollcommand=scrollbar.set)

        dict = {'Ron': 1, 'gal': 3, 'lian': 4}
        i = 50
        while i > 0:
            for key in dict:
                listNodes.insert(END, key + ' - ' + str(dict.get(key)) + '\n')
                i -= 1
        pass

    def stem_control(self):
        if self.stemming_bool:
            self.stemming_bool = False
        else:
            self.stemming_bool = True
        self.controller.set_stemming_bool(self.stemming_bool)

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

# view = IndexView("")
# view.index_view()
