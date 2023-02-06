import numpy as np

import utils


class NaiveBayes:
    def __init__(self, n_corpus, n_class, smooth_k=1):
        self.n_corpus = n_corpus
        self.n_class = n_class
        self.set_smooth_k(smooth_k)
        self.clear()
        # P_w_c = np.zeros(n_corpus, n_class)

    def clear(self):
        self.N_c = np.zeros(self.n_class, dtype=int)
        self.N_w_c = np.zeros([self.n_corpus, self.n_class], dtype=int)

    def set_smooth_k(self, k):
        self.k = k

    def finalize(self):
        P_c = self.N_c / self.N_c.sum()
        P_w_c = (self.N_w_c + self.k) / (self.N_w_c + self.k).sum(axis=0)

        self.lP_c = np.log(P_c)
        self.lP_w_c = np.log(P_w_c)

    def update(self, docs, labels):
        for doc, label in zip(docs, labels):
            self.N_c[label] += 1
            for line in doc:
                for word in line:
                    self.N_w_c[word][label] += 1
        self.finalize()

    def predict(self, docs):
        prob = [np.sum(self.lP_w_c[utils.concat_lists(*doc)],
                       axis=0) + self.lP_c for doc in docs]

        return np.argmax(prob, axis=1)
