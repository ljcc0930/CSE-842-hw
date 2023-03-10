import os

import sklearn.datasets
import sklearn.model_selection
import sklearn.feature_extraction

import nltk

from .polarity import Polarity
import utils


class SklearnPolarity:
    dataset_url = "https://www.cs.cornell.edu/people/pabo/movie-review-data/review_polarity.tar.gz"

    def __init__(self, n_folds, n_grams, data_dir):
        self.data_dir = data_dir
        self.n_folds = n_folds
        self.n_grams = n_grams
        self.n_class = 2

        self._is_encoded = False

        self.prepair_data()

    def prepair_data(self):
        dataset_url = self.dataset_url
        data_dir = self.data_dir
        dataset_compress_name = dataset_url.split('/')[-1]

        utils.ensure_download_data(
            dataset_url, data_dir, dataset_compress_name)

        dataset_dir = os.path.join(data_dir, 'txt_sentoken')
        self.dataset = sklearn.datasets.load_files(dataset_dir, shuffle=True)

    def get_datasets(self, fold):
        assert self._is_encoded

        train_idx, test_idx = self.folds[fold]

        train_text = self.encoded[train_idx]
        test_text = self.encoded[test_idx]
        train_label = self.dataset.target[train_idx]
        test_label = self.dataset.target[test_idx]

        return train_text, train_label, test_text, test_label

    def encode(self, tfidf=False):
        if self._is_encoded:
            return
        nltk.download('punkt')
        transformer = sklearn.feature_extraction.text.CountVectorizer(
            min_df=0, tokenizer=nltk.word_tokenize, ngram_range=(1, self.n_grams))
        self.encoded = transformer.fit_transform(self.dataset.data)

        if tfidf:
            transformer = sklearn.feature_extraction.text.TfidfTransformer()
            self.encoded = transformer.fit_transform(self.encoded)

        kf = sklearn.model_selection.KFold(n_splits=self.n_folds)
        self.folds = list(kf.split(self.encoded, self.dataset.target))

        self._is_encoded = True
