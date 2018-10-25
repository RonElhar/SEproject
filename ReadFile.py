import os


def createSeperatedDoc(path, filename, currentContent):
    pass


def seperateDocsInDir(path):
    docsContent =[] #This is the Array of the content of each doc (including tags);
    for filename in os.listdir(path):
        curFile = open(path+"\\"+filename+"\\"+filename,"r")
        lines = curFile.readlines()
        currentContent = ""
        for line in lines:
                currentContent.__add__(line)
                if line ==  "</DOC>":
                    docsContent.__add__(currentContent)
                    currentContent = ""
    return docsContent

                    


#problem with permissions in corpus file, couldn't make it work
seperateDocsInDir("C:\Users\USER\Desktop\SearchEngine\corpus")
