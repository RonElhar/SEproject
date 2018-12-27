from math import log10
from operator import itemgetter


def calculate_tf_idf(tf, df, doc_length, num_of_docs):
    return (float(tf) / doc_length) * (log10(num_of_docs / float(df)))


class Ranker:
    def __init__(self, avg_doc_length):
        self.k = 1.2
        self.b = 0.75
        self.avdl = avg_doc_length

    def rank_doc(self, query_dict, words_dict, docs_dict):
        result = {}
        for word in words_dict:
            for doc in words_dict[word]:
                if doc not in result:
                    tf_idf = calculate_tf_idf(words_dict[word][doc][0], len(words_dict[word]), docs_dict[doc].length,
                                              len(docs_dict))

                    result[doc] = tf_idf + self.rank_bm25(len(words_dict[word]), words_dict[word][doc][0], query_dict[word], docs_dict[doc].length, len(docs_dict))
                else:
                    tf_idf = calculate_tf_idf(words_dict[word][doc][0], len(words_dict[word]), docs_dict[doc].length,
                                              len(docs_dict))
                    result[doc] += tf_idf + self.rank_bm25(len(words_dict[word]), words_dict[word][doc][0], query_dict[word], docs_dict[doc].length, len(docs_dict))
                # if word in docs_dict[doc].title:
                #     result[doc] *= 1.5
                # loc = words_dict[word][doc][1]
                # if loc[0] < docs_dict[doc].length / 5:
                #     result[doc] *= 1.2
        result = sorted(result.items(), key = itemgetter(1))
        final = []
        i = len(result) - 1
        while i >= len(result) - 50 and i >= 0:
            final.append(result[i])
            i -= 1
        return final

    def compute_k(self, dl):
        return self.k * ((1 - self.b) + self.b * (float(dl) / float(self.avdl)))

    def rank_bm25(self, word_df, doc_freq, query_freq, dl, num_of_docs):
        k = self.compute_k(dl)
        log_part = log10(float(num_of_docs + 1) / float(word_df))
        middle_part = float((self.k + 1) * doc_freq) / float(k + doc_freq)
        return float(query_freq) * middle_part * log_part
