import nltk
import numpy as np
from nltk.stem import SnowballStemmer


stemmer = SnowballStemmer("spanish")


def ensure_nltk_data():
    resources = {
        "tokenizers/punkt": "punkt",
    }

    for resource_path, package_name in resources.items():
        try:
            nltk.data.find(resource_path)
        except LookupError:
            nltk.download(package_name)


def tokenize(sentence):
    return nltk.word_tokenize(sentence.lower(), language="spanish")


def normalize_words(words, ignore_words=None):
    ignore_words = ignore_words or set()
    return [
        stemmer.stem(word.lower())
        for word in words
        if word not in ignore_words and word.isalpha()
    ]


def bag_of_words(sentence, vocabulary):
    sentence_words = normalize_words(tokenize(sentence))
    bag = [1 if word in sentence_words else 0 for word in vocabulary]
    return np.array(bag, dtype=np.float32)
