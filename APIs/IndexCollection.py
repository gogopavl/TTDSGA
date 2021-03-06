import json, re
import urllib
import pandas as pd
from pandas.io.json import json_normalize
from nltk.stem import PorterStemmer
from AnalysedTweet import AnalysedTweet

class IndexCollection():
    """inverted index based on words from caption,tags from API + text"""
    def __init__(self):
        self.iid ={}
        self.stem = PorterStemmer()
        self.stopwords = self.listtostop()
        
    def load(self, instance):
        return instance

    def add_tweet(self, atweet):
        tweetID = atweet.Id
        # Index tweet text
        for term in filter(None, self.tokenize(atweet.text)):
            if self.rid_stopword(term):
                key = self.stemming(term)
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else:
                    self.iid[key] = [tweetID]
        # TODO: index vision results etc.
        # tags
        # for tag in vision.tags:
        #     tag.confidence, tag.name
        # captions
        # for caption in vision.description.captions:
        #     caption.confidence, caption.text
        

    def collect_label(self, tweetandvision):
        """tags: cut above the confidence 50
            key of list of dictionaries with 'confidence' and 'name'"""

        #tags from image!
        tweetID = tweetandvision['Tweet']['ID']
        for item in tweetandvision['VisionResults']['tags']:
            if item['confidence']>0.5:
                key= item['name']
                #costly to process the entier thing?
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else: #given each tweetID will be unique
                    self.iid[key].append(tweetID)

        #caption from image!
        caption = tweetandvision['VisionResults']['description']['captions'][0]['text']
        for term in filter(None, self.tokenize(caption)):
            if self.rid_stopword(term):
            #should save just a bit of calculation in this step
                key = self.stemming(term)
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else:
                    self.iid[key].append(tweetID)

        #text!
        tweettext = tweetandvision['Tweet']['Text']
        for term in filter(None, self.tokenize(tweettext)):
            if self.rid_stopword(term):
                key = self.stemming(term)
                if key not in self.iid:
                    self.iid[key] = [tweetID]
                else:
                    self.iid[key] = [tweetID]


    def stemming(self,term):
        return self.stem.stem(term)

    def tokenize(self,content):
        content = content.lower()
        content = re.compile("s\'s\\b").sub("s",content)
        content = re.compile("'").sub("",content)
        content = re.compile("[^\W\s]").sub(" ", content)
        content = content.split()
        return content

    def listtostop(self):
        stop = urllib.request.urlopen('http://members.unine.ch/jacques.savoy/clef/englishST.txt') 
        stopwords = stop.read().decode('utf-8') 
        return self.tokenize(stopwords)
    
    def rid_stopword(self, word):
        if word in self.stopwords:
            return False
        return True

    def preprocess(self, text):
        terms = self.tokenize(text)
        terms = self.rid_stopwords(terms)
        terms = self.stemming(terms)
        return terms


    def main(self, direc):
        #given multiple files in direc
        ds = self.load('temp')
        self.collect_label(ds)
            
    def update(self, _tweets):
        #self.iid
        #how to get realtime tweets

        new_ds = self.load(_tweets)
        self.collect_label(new_ds)

    def export(self):
        return self.iid


if __name__ == '__main__':
    directory ='typein_repo_address'
    db = IndexCollection()
    db.main(directory)
    print(db.iid)
#to send to in-memory DB, fill in the git connected to Heroku
