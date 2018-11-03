from Tkinter import *
import tkFileDialog

from Main import Main


def make_entry(parent, caption, row, column, width=None, **options):
    Label(parent, text=caption).grid(row=row, column=column)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.grid(row=row, column=column + 1)
    return entry


class GuiControl:
    def __init__(self, main):
        self.main = main
        self.corpus_path = ''
        self.posting_path = ''
        self.stemming_bool = False
        self.search_window = Tk()
        self.welcome_window = Tk()

    def browse_corpus_dir(self):
        dir_name = tkFileDialog.askdirectory()
        self.corpus_e.insert(0, dir_name)

    def browse_posting_dir(self):
        dir_name = tkFileDialog.askdirectory()
        self.posting_path.insert(0, dir_name)

    ### implement this:
    def continue_try(self):
        # check valid paths
        Main.continue_try(main, self.corpus_path, self.posting_path)
        pass

    def search_view(self):
        self.search_window.title("Documents Search Engine")
        self.search_window.config(bg="LightBlue")
        stemming_radio = Radiobutton(master=self.search_window, text="Preform Stemming")
        reset_b = Button(master=self.search_window, text='Reset', width=6, command=self.reset)
        load_dict = Button(master=self.search_window, text="Load Dictionary")
        show_dict = Button(master=self.search_window, text="Show Dictionary")
        query_e = Entry(master=self.search_window)
        search_b = Button(master=self.search_window, text="")

    def reset(self):
        pass

    def welcome(self):
        self.welcome_window.title("Welcome!")
        self.welcome_window.config(bg="LightBlue")
        corpus_e = make_entry(self.welcome_window, "Corpus Path:", 1, 0, 60)
        posting_path = make_entry(self.welcome_window, "Posting Path:", 2, 0, 60)
        continue_button = Button(master=self.welcome_window, text='Start', width=6, command=self.start)
        continue_button.grid(row=3, column=1)
        welcome_instruction = Label(master=self.welcome_window,
                                    text='Hello! In order to proceed, please insert Corpus and Posting paths:')
        welcome_instruction.grid(row=0, column=1)
        browse_corpus = Button(master=self.welcome_window, text='Browse', width=6, command=self.browse_corpus_dir)
        browse_corpus.grid(row=1, column=3)
        browse_posting = Button(master=self.welcome_window, text='Browse', width=6, command=self.browse_posting_dir)
        browse_posting.grid(row=2, column=3)
        self.welcome_window.mainloop()
