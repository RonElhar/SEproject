import os
from ReadFile import ReadFile
from Parse import Parse
from ReadFile import Document

class Main:
    def __init__(self):
        self.reader = ReadFile()
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.parser = Parse()

    def start(self):
        for filename in os.listdir(self.ROOT_DIR):
            self.reader.separate_docs_in_file(self.ROOT_DIR,filename)
