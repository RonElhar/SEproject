import os
import re


class ReadFile:

    def __init__(self):
        self.cities = set()
        self.languages = set()
        pass

    # def read_directory_files(self, path):
    #     files = {}
    #     docs = []
    #     for filename in os.listdir(path):
    #         files.__setitem__(filename, self.separate_docs_in_file(path, filename))
    #     return files

    def separate_docs_in_file(self, path, filename):
        docs = {}  # This is the Array of the content of each doc (including tags);
        doc_index = 0
        cur_file = open(path + "\\" + filename + "\\" + filename, "r")
        lines = cur_file.readlines()
        doc_text = ""
        doc_id = ""
        doc_city = ""
        doc_title = ""
        doc_date = ""
        is_text = False
        for i in range(len(lines)):
            line = lines[i]
            if line.__contains__("</TEXT>"):
                is_text = False
            if is_text:
                doc_text += line.replace('\n', ' ')
                continue
            if line.__contains__("<DOC>"):
                doc_text = ""
                doc_id = ""
                doc_city = ""
                doc_title = ""
                doc_date = ""
                doc_index += 1
                continue
            if line.__contains__("</DOC>"):
                docs[doc_id] = Document(doc_id, doc_date, doc_title, doc_city, doc_text)
                continue
            if line.__contains__("<DOCNO>"):
                line = line.replace("<DOCNO>", '')
                line = line.replace("</DOCNO>", '')
                doc_id = line.replace('\n', '')
                continue
            if line.__contains__("<TI>"):
                line = line.replace("<TI>", '')
                line = line.replace("</TI>", '')
                line = line.replace("<H3>", '')
                line = line.replace("</H3>", '')
                doc_title = line.replace('\n', '')
                continue
            if line.__contains__('<F P=104>'):
                temp = line.split('>')
                temp = temp[1].split('<')
                temp = temp[0].split(' ')
                doc_city = temp[0]
                self.cities.add(doc_city)
            if line.__contains__('<DATE1>'):
                line = line.replace('<DATE1>', '')
                line = line.replace('</DATE1>', '')
                doc_date = line.replace('\n', '')
                continue
            if line.__contains__("<TEXT>"):
                is_text = True
                if lines[i + 1].__contains__('Language: <F P=105>'):
                    temp = lines[i + 1].split('>')
                    temp = temp[1].split('<')
                    temp = temp[0].split(' ')
                    language = temp[0]
                    self.languages.add(language)
                    lines[i + 1] = ' '
                if lines[i + 4].__contains__('<F P=106>'):
                    lines[i + 4] = lines[i + 4].replace('<F P=106>', '')
                    lines[i + 4] = lines[i + 4].replace('</F>', '')
        cur_file.close()
        return docs


class Document:
    def __init__(self, doc_id, date, title, city, text):
        self.id = doc_id
        self.date = date
        self.title = title
        self.origin_city = city
        self.length = 0
        self.text = text
        self.max_tf = 0
        self.num_of_unique_words = 0

    def set_length(self, length):
        self.length = length

    def tostr(self):
        return self.id + ', ' + self.title
