import os
import re


class ReadFile:

    def createSeperatedDoc(path, filename, currentContent):
        pass

    def seperateDocsInDir(path):
        docsContent = []  # This is the Array of the content of each doc (including tags);
        for filename in os.listdir(path):
            curFile = open(path + "\\" + filename + "\\" + filename, "r")
            lines = curFile.readlines()
            currentContent = []
            for line in lines:
                currentContent.append(line)
                if line.__contains__("</DOC>"):
                    docsContent.append(currentContent)
                    return docsContent[0]
                    # currentContent = ""
        # print(docsContent[0])
        # return docsContent


    def getText(self):
        docText = ""
        isText = False
        docContent = self.seperateDocsInDir("C:\Users\USER\Desktop\SearchEngine\corpus")
        for line in docContent:
            if line.__contains__("</TEXT>"):
                isText = False
            if isText:
                docText += line
            if line.__contains__("<TEXT>"):
                isText = True
        return docText


    def getTerms(self,text):
        terms = str.split(text, " ")
        terms = filter(None, terms)
        tCount = 0
        for term in terms:
            terms[tCount] = re.sub('[^A-Za-z0-9\-$%/.]+', '', term)
            if not re.match("^\d+?\.\d+?$", terms[tCount]) and not re.match(r'^\d+/\d+$', terms[tCount]):
                terms[tCount] = re.sub('[^A-Za-z0-9\-$%]+', '', terms[tCount])
            if tCount + 1< terms.__len__() and re.match(r'^\d+/\d+$', terms[tCount+1]):
                    terms[tCount] += ' ' + terms[tCount+1]
                    terms[tCount+1] = ''
            terms[tCount] = terms[tCount].replace('\n', '')
            tCount += 1
        terms = filter(None, terms)
        return terms

reader = ReadFile()
reader.getTerms("23.4, 25, 3/4")
# seperateDocsInDir("C:\Users\USER\Desktop\SearchEngine\corpus")
