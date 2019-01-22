import os, re
from stemming.porter2 import stem

class PreProcessor:
    _stopwords_file = os.getcwd() + r"\Search\files\stopwords.txt"

    def process(self, text):
        """ Apply all default pre-processing. """
        tokens = self.tokenize(text)
        tokens = self.remove_stopwords(tokens)
        tokens = self.apply_stemming(tokens)
        return tokens

    def tokenize(self, text):
        t = text.lower()

        # Replace "s's" at the end of a word with "s"
        t = re.compile("s\'s\\b").sub("s", t)

        # Remove apostrophes to avoid splitting on them
        t = re.compile("'").sub("", t)

        # Replace all other non-word, non-space characters with spaces so we can split on them
        t = re.compile("[^\w\s]").sub(" ", t)

        # Get individual words
        tokens = t.split()        
        return tokens

    def remove_stopwords(self, tokens):
        stop_file = open(self._stopwords_file).read()
        stopwords = self.tokenize(stop_file)

        result = [token for token in tokens if token not in stopwords]
        return result

    def apply_stemming(self, tokens):
        return list(stem(t) for t in tokens)