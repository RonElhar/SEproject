import gensim
from gensim.models import Word2Vec
from ReadFile import ReadFile
import os


class Semantics:
    def __init__(self):
        self.reader = ReadFile()
        self.path = 'D:\\Studies\\BGU\\semesterE\\IR\\IRProj\\SEproject\\corpus'
        self.sentences = []

    def read_corpus(self):
        i = 0
        dirs_list = os.listdir(self.path)

        while i < 3: # len(dirs_list)
            docs = self.reader.separate_docs_in_file(self.path, dirs_list[i])
            for doc_id in docs:
                terms = gensim.utils.simple_preprocess(docs[doc_id].text)
                self.sentences.append(terms)
            i += 1
            docs.clear()

    def start(self):
        # train model
        # model = Word2Vec(self.sentences, min_count=2)
        #model = gensim.models.Word2Vec(documents, size=150, window=10, min_count=2, workers=10)
        # model.train(self.sentences, total_examples=len(self.sentences), epochs=10)
        # save model
        # model.save('model.bin')
        # load model
        new_model = Word2Vec.load('model.bin')
        # access vector for one word
        w1 = 'intelligence'
        similar = new_model.wv.most_similar(positive=w1)
        print similar

# text = '<F P=106> [Article by Ovidio Bellando] </F> [Text]  "he is absolutely convinced" that Great Britain "sees" Argentine-Chilean relations with good eyes. to cooperate over oil exploration...if that is possible.Chile, if facts kept in absolute secrecy until 4 March are'
# terms = gensim.utils.simple_preprocess(text)
# tokens = gensim.utils.simple_tokenize(text)
# print terms
sem = Semantics()
#sem.read_corpus()
sem.start()