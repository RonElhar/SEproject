from math import log

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
                    result[doc] = self.rank_BM25(len(words_dict[word]), words_dict[word][doc][0], query_dict[word][0],
                                                 docs_dict[doc][1])
                else:
                    result[doc] += self.rank_BM25(len(words_dict[word]), words_dict[word][doc][0], query_dict[word][0],
                                                  docs_dict[doc][1])
        return result # sort by keys

    def compute_K(self, dl):
        return self.k * ((1 - self.b) + self.b * (float(dl) / float(self.avdl)))

    def rank_BM25(self, word_df, doc_freq, query_freq, dl):
        K = self.compute_K(dl)
        log_part = log(float(self.num_of_docs + 1) / float(word_df))
        middle_part = ((self.k + 1) * doc_freq) / (K + doc_freq)
        return query_freq * middle_part * log_part