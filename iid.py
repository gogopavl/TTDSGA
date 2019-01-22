import json, re
import urllib
import pandas as pd
from pandas.io.json import json_normalize
from nltk.stem import PorterStemmer


class dailybatch():
    """inverted index based on words from caption,tags from API + text"""
    def __init__(self):
        self.iid ={}
        self.stem = PorterStemmer()

    def load(self, link):

        with open('toydata.json') as tdata:
            red = json.load(tdata)
        return red 

    def collect_label(self, jsondic):
        """tags: cut above the confidence 50
            key of list of dictionaries with 'confidence' and 'name'"""

        tweetID =jsondic['requestId']
        for item in jsondic['tags']:
            if item['confidence']>0.5:
                key= item['name']
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else: #given each tweetID will be unique
                    self.iid[key].append(tweetID)

        caption = jsondic['description']['captions'][0]['text']
        for term in filter(None, self.tokenize(caption)):
            term = self.stemming(term)
            print('each term', term)
            if self.rid_stopword(term):
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else:
                    self.iid[key].append(tweetID)


    def stemming(self,term):
        return self.stem.stem(term)

    def tokenize(self,content):
        return re.split(r'\W+', content)

    def stopwords(self):
        f = urllib.request.urlopen('http://members.unine.ch/jacques.savoy/clef/englishST.txt') 
        text_to_parse = f.read().decode('utf-8') 
        self.words = set(filter(None, re.split(r'\r\n', text_to_parse)))

    def rid_stopword(self, word):
        if word in self.words:
            return False
        return True


    def main(self, direc):
        self.stopwords() #creates words to filter out 
        #given multiple files in direc
        #for each in direc:
        ds = self.load('temp')
        self.collect_label(ds)
            
    def update(self, _tweets):
        #self.iid
        #how to get realtime tweets

        new_ds = self.load(_tweets)
        self.collect_label(new_ds)


if __name__ == '__main__':
    directory ='typein_repo_address'
    db = dailybatch()
    db.main(directory)
    print(db.iid)
#to send to in-memory DB, fill in the git connected to Heroku
