import os


def createSeperatedDoc(path, filename, currentContent):
    pass


def seperateDocsInDir(path):
    for filename in os.listdir(path):
        curFile = open(path+"\\"+filename+"\\"+filename,"r")
        lines = curFile.readlines()
        currentContent = ""
        for line in lines:
            if line == "<Doc>":
                currentContent.__add__(line)


                    


#problem with permissions in corpus file, couldn't make it work
seperateDocsInDir("C:\Users\USER\Desktop\SearchEngine\corpus")
