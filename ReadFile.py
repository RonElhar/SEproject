import os
import re


def createSeperatedDoc(path, filename, currentContent):
    pass


def seperateDocsInDir(path):
    docsContent =[] #This is the Array of the content of each doc (including tags);
    for filename in os.listdir(path):
        curFile = open(path+"\\"+filename+"\\"+filename,"r")
        lines = curFile.readlines()
        currentContent = []
        for line in lines:
                currentContent.append(line)
                if  line.__contains__("</DOC>"):
                    docsContent.append(currentContent)
                    return docsContent[0]
                    #currentContent = ""
    #print(docsContent[0])
    #return docsContent

def getText():
    docText = ""
    isText = False
    docContent = seperateDocsInDir("C:\Users\USER\Desktop\SearchEngine\corpus")
    for line in docContent:
        if line.__contains__("</TEXT>"):
            isText = False
        if isText:
            docText+=line
        if line.__contains__("<TEXT>"):
            isText = True
    return docText

def getTerms(text):
    terms = str.split(text," ")
    tCount=0
    for term in terms:
        terms[tCount] = re.sub('[^A-Za-z0-9\-$%/]+', '', term)
        if terms[tCount].isdigit() == False and terms[tCount].__contains__('.') :
            terms[tCount] = terms[tCount].replace('.', '')
        if terms[tCount].isdigit() and terms[tCount].__contains__('.'):
            print(terms[tCount])
        terms[tCount] = terms[tCount].replace('\n','')
        tCount+=1
    terms = filter(None, terms)
    return terms




                    

getTerms(getText())
#seperateDocsInDir("C:\Users\USER\Desktop\SearchEngine\corpus")
