import gensim
from gensim.models import Word2Vec
from ReadFile import ReadFile
import datetime
import os


class Semantics:
    def __init__(self):
        self.reader = ReadFile()
        self.path = 'C:\\Users\\ronelhar\\PycharmProjects\\SEproject\\corpus'
        self.sentences = []

    def read_corpus(self):
        i = 0
        dirs_list = os.listdir(self.path)

        while i < len(dirs_list):  # len(dirs_list)
            docs = self.reader.separate_docs_in_file(self.path, dirs_list[i])
            j = 0
            for doc_id in docs:
                terms = gensim.utils.simple_preprocess(docs[doc_id].text)
                self.sentences.append(terms)
                j += 1

            i += 1
            docs.clear()

    def start(self):
        # train model
        print "finished read"
        # model = Word2Vec(self.sentences, min_count=5)
        model = gensim.models.Word2Vec(self.sentences, size=150, window=10, min_count=5, workers=10)
        model.train(self.sentences, total_examples=len(self.sentences), epochs=10)
        # save model
        model.save('model.bin')
        # load model
        new_model = Word2Vec.load('model.bin')
        # access vector for one word
        w1 = 'intelligence'
        similar = new_model.wv.most_similar(positive=w1)
        print similar


print datetime.datetime.now()
sem = Semantics()
sem.read_corpus()
sem.start()
print datetime.datetime.now()
