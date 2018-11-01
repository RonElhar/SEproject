import os
import re


class ReadFile:

    def __init__(self):
        pass

    def read_directory_files(self, path):
        files = {}
        docs = []
        for filename in os.listdir(path):
            files.__setitem__(filename, self.separate_docs_in_file(path, filename))
        return files

    def separate_docs_in_file(self, path, filename):
        docs = []  # This is the Array of the content of each doc (including tags);
        doc_index = 0
        cur_file = open(path + "\\" + filename + "\\" + filename, "r")
        lines = cur_file.readlines()
        current_content = []
        doc_text = ""
        doc_name = ""
        doc_id = ""
        doc_city = ""
        doc_title = ""
        doc_date = ""
        is_text = False
        for line in lines:
            if line.__contains__("</TEXT>"):
                is_text = False
            if is_text:
                doc_text += line
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
                docs.append(Document(doc_id, doc_date, doc_title, doc_city, doc_text))
                continue
            if line.__contains__("<DOCNO>"):
                line = line.replace("<DOCNO>", '')
                line = line.replace("</DOCNO>", '')
                doc_id = line.replace('\n','')
                continue
            if line.__contains__("<TI>"):
                line = line.replace("<TI>", '')
                line = line.replace("</TI>", '')
                line = line.replace("<H3>", '')
                line = line.replace("</H3>", '')
                doc_title = line.replace('\n','')
                continue
            if line.__contains__('<F P=104>'):
                temp = line.split('>')
                temp = temp[1].split('<')
                temp = temp[0].split(' ')
                doc_city = temp[0]
            if line.__contains__('<DATE1>'):
                line = line.replace('<DATE1>', '')
                line = line.replace('</DATE1>', '')
                doc_date = line.replace('\n','')
                continue
            if line.__contains__("<TEXT>"):
                is_text = True
        return docs
    @staticmethod
    def get_text(doc_content):
        doc_text = ""
        is_text = False
        for line in doc_content:
            if line.__contains__("</TEXT>"):
                is_text = False
            if is_text:
                doc_text += line
            if line.__contains__("<TEXT>"):
                is_text = True
        return doc_text

    def get_terms(self, text):
        terms = str.split(text, " ")
        terms = filter(None, terms)
        tCount = 0
        for term in terms:
            terms[tCount] = re.sub('[^A-Za-z0-9\-$%/.]+', '', term)
            if not re.match("^\d+?\.\d+?$", terms[tCount]) and not re.match(r'^\d+/\d+$', terms[tCount]):
                terms[tCount] = re.sub('[^A-Za-z0-9\-$%]+', '', terms[tCount])
            if re.match(r'^\d+\d+$', terms[tCount]) and tCount + 1 < terms.__len__() and re.match(r'^\d+/\d+$',
                                                                                                  terms[tCount + 1]):
                terms[tCount] += ' ' + terms[tCount + 1]
                terms[tCount + 1] = ''
            if term.__contains__('-') and not re.search('[a-zA-Z]', term) and not re.search('[0-9]', term):
                terms.__delitem__(tCount)
            elif term.__contains__('-'):
                words = str.split(term, '-')
                if words[words.__len__() - 1] == '':
                    terms[tCount] = terms[tCount].replace('-', '')
            terms[tCount] = terms[tCount].replace('\n', '')
            tCount += 1
        terms = filter(None, terms)
        return terms


class Document:
    def __init__(self, doc_id, date, title, city, text):
        self.id = doc_id
        self.date = date
        self.title = title
        self.origin_city = city
        self.length = 0
        self.text = text

    def set_length(self, length):
        self.length = length


reader = ReadFile()
reader.read_directory_files(os.path.dirname(os.path.abspath(__file__)) + '\\corpus')
