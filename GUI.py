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

    def browse_corpus_dir(self):
        dir_name = tkFileDialog.askdirectory()
        self.corpus_entry.insert(0, dir_name)

    def browse_posting_dir(self):
        dir_name = tkFileDialog.askdirectory()
        self.posting_entry.insert(0, dir_name)

    def reset(self):
        # self.controller.reset()
        pass

    def start(self):
        # self.controller.start(self.corpus_entry.get(), self.posting_entry.get(),self.stemming_bool)
        pass

    def load(self):
        # self.controller.load(self.posting_entry.get())
        pass

    def show(self):
        dict_window = Tk()
        i = 30
        # dict = sorted(self.controller.get_dict())
        dict = {'Ron': 1, 'gal': 3, 'lian': 4, }
        scrollbar = Scrollbar(master=dict_window)
        text_display = Text(master=dict_window)
        scrollbar.pack(side=RIGHT, fill=Y)
        text_display.pack(side=LEFT, fill=Y)
        scrollbar.config(command=text_display.yview())
        text_display.config(yscrollcommand=scrollbar.set)

        while i > 0:
            for key in dict:
                text_display.insert(END, key + ' - ' + str(dict.get(key)) + '\n')
                i -= 1
        pass

    def stem_control(self):
        if self.stemming_bool:
            self.stemming_bool = False
        else:
            self.stemming_bool = True
        print(self.stemming_bool)

    def index_view(self):
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
        language_list = Listbox(master=self.index_window)
        language_list.insert(END, "English")
        Label(master=self.index_window, text="Languages:").grid(row=4, column=1, sticky='W')
        language_list.grid(row=5, column=1, sticky='W')
        load_dict_button = Button(master=self.index_window, text="Load Dictionary", command=self.load)
        load_dict_button.grid(row=4, column=1, sticky='E')
        show_dict_button = Button(master=self.index_window, text="Show Dictionary", command=self.show)
        show_dict_button.grid(row=4, column=2)
        reset_button = Button(master=self.index_window, text='Reset', width=6, command=self.reset)
        reset_button.grid(row=4, column=3)
        self.index_window.mainloop()


#view = IndexView("")
#view.index_view()
