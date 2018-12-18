from math import log
from operator import itemgetter


class Ranker:
    def __init__(self):
        self.k = 2
        self.b = 0.75
        self.num_of_docs = 472525
        self.avdl = 253

    def rank_doc(self, query_dict, words_dict, docs_dict):
        result = {}
        for word in query_dict:
            for doc in words_dict[word]:
                if doc not in result:
                    result[doc] = self.rank_BM25(len(words_dict[word]), words_dict[word][doc][0], query_dict[word],
                                                 docs_dict[doc][1])
                else:
                    result[doc] += self.rank_BM25(len(words_dict[word]), words_dict[word][doc][0], query_dict[word],
                                                  docs_dict[doc][1])
        result = sorted(result.items(), key=itemgetter(1))
        final = []
        i = len(result) - 1
        while i >= len(result) - 200:
            final.append(result[i])
            print result[i]
            i -= 1
        return final

    def compute_K(self, dl):
        return self.k * ((1 - self.b) + self.b * (float(dl) / float(self.avdl)))

    def rank_BM25(self, word_df, doc_freq, query_freq, dl):
        K = self.compute_K(dl)
        log_part = log(float(self.num_of_docs + 1) / float(word_df))
        middle_part = float((self.k + 1) * doc_freq) / float(K + doc_freq)
        return float(query_freq) * middle_part * log_part