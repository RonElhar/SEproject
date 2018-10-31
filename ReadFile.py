import os
import re


class ReadFile:

    def createSeperatedDoc(path, filename, currentContent):
        pass

    def seperateDocsInDir(self, path):
        docs_content = []  # This is the Array of the content of each doc (including tags);
        for filename in os.listdir(path):
            cur_file = open(path + "\\" + filename + "\\" + filename, "r")
            lines = cur_file.readlines()
            current_content = []
            for line in lines:
                current_content.append(line)
                if line.__contains__("</DOC>"):
                    docs_content.append(current_content)
                    return docs_content[0]
                    # current_content = ""
        # print(docs_content[0])
        # return docs_content

    def get_text(self):
        doc_text = ""
        isText = False
        doc_content = self.seperateDocsInDir("C:\\Users\\ronel\\Desktop\\Search Engine\\corpus")
        for line in doc_content:
            if line.__contains__("</TEXT>"):
                isText = False
            if isText:
                doc_text += line
            if line.__contains__("<TEXT>"):
                isText = True
        return doc_text

    def getTerms(self, text):
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

# reader = ReadFile()
# terms = reader.getTerms(reader.getText())
# 3var = ""
