import os
import re

"""
~~~~~~~~~~~~~~~~~~~~~~~~  Module Description ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This Module is used for getting documents texts and more info about the documents in the corpus .


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


class ReadFile:
    """
       Class Description :
           This Class is used for getting info and seperating documents from files
    """

    def __init__(self):
        self.cities = {}
        self.languages = set()
        pass

    """
        Description :
            This method separates documents in a given file, and creating object for each document
        Args:
            param1 : Path of the file 
            param2 : The name of the file
 
        Returns:
            Dictionaries of documents - key = document id , value = Document object
    """

    def separate_docs_in_file(self, path, filename):
        docs = {}
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
                docs[doc_id] = Document(filename, doc_id, doc_date, doc_title, doc_city, doc_text)
                continue
            if line.__contains__("<DOCNO>"):
                line = line.replace("<DOCNO>", '')
                line = line.replace("</DOCNO>", '')
                doc_id = line.replace('\n', '').replace(' ', '')
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
                for s in temp:
                    if not s == ' ' and not s == '':
                        doc_city = temp[2].upper()
                if not doc_city in self.cities:
                    self.cities[doc_city] = [doc_id]
                else:
                    self.cities[doc_city].append(doc_id)
            if line.__contains__('<DATE>') or line.__contains__('<DATE1>'):
                no1 = False
                if line.__contains__('<DATE>'):
                    no1 = True
                line = line.replace('<DATE>', '') if no1 else line.replace('<DATE1>', '')
                line = line.replace('</DATE>', '') if no1 else line.replace('</DATE1>', '')
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
                if lines[i + 2].__contains__("Article Type"):
                    lines[i + 2] = ''
                if lines[i + 4].__contains__('<F P=106>'):
                    lines[i + 4] = lines[i + 4].replace('<F P=106>', '')
                    lines[i + 4] = lines[i + 4].replace('</F>', '')
        cur_file.close()
        return docs

    """
        Description :
            This method Gets Cities that appear in the given file
        Args:
            param1 : Path of the file 
            param2 : The name of the file
        Returns:
            Dictionary of dictionaries that where created by the processes
    """

    def read_cities(self, path, filename):
        with open(path + "\\" + filename + "\\" + filename, "r") as f:
            lines = f.readlines()
            doc_city = ""
            doc_id = ""
            for i in range(len(lines)):
                line = lines[i]
                if line.__contains__("<DOC>"):
                    doc_id = ""
                    doc_city = ""
                if line.__contains__("<DOCNO>"):
                    line = line.replace("<DOCNO>", '')
                    line = line.replace("</DOCNO>", '')
                    doc_id = line.replace('\n', '')
                if line.__contains__('<F P=104>'):
                    temp = line.split('>')
                    temp = temp[1].split('<')
                    temp = temp[0].split(' ')
                    for s in temp:
                        if not s == ' ' and not s == '':
                            doc_city = temp[2].upper()
                    if doc_city not in self.cities:
                        self.cities[doc_city] = [doc_id]
                    else:
                        self.cities[doc_city].append(doc_id)


class Document:
    """
       Class Description :
           This class Represnents a document
    """

    """
        Description
        Initializing a documnent and its properties
    """

    def __init__(self, name, doc_id, date, title, city, text):
        self.file_name = name
        self.id = doc_id
        self.date = date
        self.title = title.upper()
        self.origin_city = city
        self.length = 0
        self.max_tf = 0
        self.num_of_unique_words = 0
        self.text = text
        self.five_entities = []

    """
        Description
        Sets the length of the document 
    """

    def set_length(self, length):
        self.length = length

    """
        @overriding str method
        Creates a string representation for document object
    """

    def __str__(self):
        return self.id + ', ' + self.title
