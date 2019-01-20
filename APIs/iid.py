import json
import pandas as pd
from pandas.io.json import json_normalize
from nltk.stem import PorterStemmer


class dailybatch():
    'inverted index based on words from caption,tags from API + text'
    def __init__():
        self.iid ={}
        self.stem = PorterStemmer()

    def load(self):
    'later replace with path, and take as parameter to process multiple files'
        with open('toydata.json') as tdata:
            red = json.load(tdata)
        "json file will be read in dictionary
         per API results at least: 
        metadata = size, filetype of picture
        description -> preprocess 'captions', forget about 'tags'(too many, no numeral)"
        return red 

    def collect_label(self, jsondic):
        "tags: cut above the confidence 50%
        key of list of dictionaries with 'confidence' and 'name'"

        "hypothetical tweetID"
        tweetID =jsondic['requestID']
        for item in jsondic['tags']:
            if item['confidence']>0.5:
                key= item['name']
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else: #given each tweetID will be unique
                    self.iid[key].append(tweetID)

        caption = jsondic['description']['captions']['text']
        for term in filter(None, self.tokenize(caption):
            term = self.stemming(term)
            if self.rid_stopword(term):
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else:
                    self.iid[key].append(tweetID)


    def stemming(self,term):
    'run the Porerstemmer'
        return self.stem.stem(term)

    def tokenize(self,content):
    'tokenize on non-alphabetical character'
        return re.split(r'\W+', content)

    def stopwords(self):
    'the list of stop words from the link will be used to reduce the number of words we keep in our index'
        f = urllib.request.urlopen('http://members.unine.ch/jacques.savoy/clef/englishST.txt') 
        text_to_parse = f.read().decode('utf-8') 
        self.words = set(filter(None, re.split(r'\r\n', text_to_parse)))

    def rid_stopword(self, word):
    'criteria to check whether we keep the word or not in the index'
        if word in self.words:
            return False
        return True


    def main(self):
        self.stopwords() #creates words to filter out 
        #given multiple files in direc
        for each in direc:
            ds = load()
            
    def dumptofile(self):
        pass 


if __name__ == '__main__':
    db = dailybatch()
    db.main()
    #db.iid
#to send to in-memory DB
