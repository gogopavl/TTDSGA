import sys, time, json
import tweepy
import secrets
from collections import namedtuple
from MS_Vision import getImageResults

class MyStreamListener(tweepy.StreamListener):
    _maxTweets = 1
    _tweetCount = 0
    
    def __init__(self, api=None, maxTweets=1):
        self._maxTweets = maxTweets
        self._tweetCount = 0
        super().__init__(api=api)

    def on_status(self, status):      
        media = self.get_media(status)
        if media is None:
            return

        tweet = Tweet()
        tweet.Text = status.text
        tweet.Url = media["url"]
        tweet.ImageUrl = media["media_url_https"]
        
        # Call vision API
        vision_json = getImageResults(tweet.ImageUrl)
        vision = json.loads(vision_json, object_hook=lambda obj: namedtuple('result', obj.keys())(*obj.values()))
        
        ## Display to console for now
        print(tweet.Url)
        print(tweet.Text)
        print(tweet.ImageUrl)
        print("Tags:")
        for tag in vision.tags:
            print("{0:.00%} : {1}".format(tag.confidence, tag.name))
        print("Captions")
        for caption in vision.description.captions:
            print("{0:.00%} : {1}".format(caption.confidence, caption.text))

        ## Check count to limit utilization while in development
        self._tweetCount += 1
        if self._tweetCount >= self._maxTweets:
            return False

    def on_error(self, status_code):
        print("Error: {0}".format(status_code))
        if status_code == 420:
            # Enhance your calm; stop processing to avoid exponential wait time increases
            # Need better handling
            return False

    def on_limit(self, track):
        print("Limit reached")
        # Stop processing as soon as we hit a limit to avoid exponential wait time increases
        # Need better handling
        return False

    def get_media(self, status):
        if status.lang != "en":
            return

        # Exclude possibly NSFW tweets
        if hasattr(status, "possibly_sensitive") and status.possibly_sensitive:
            return
        
        # We only want tweets with images
        if not hasattr(status, "entities"):
            return
        entities = status.entities

        if not "media" in entities.keys():
            return
        media = entities["media"]

        if len(media) < 1:
            return

        media = media[0]

        if not "media_url_https" in media.keys() or "url" not in media.keys():
            return
        
        return media

class Tweet:    
    def __init__(self, text=None, url=None, imageUrl=None, hashTags=[]):
            self.Text = text
            self.Url = url
            self.ImageUrl = imageUrl
            self.Hashtags = hashTags
            return

class StreamBuilder():
    # From http://techland.time.com/2009/06/08/the-500-most-frequently-used-words-on-twitter/
    topTerms = ['the','i','to','a','and','is','in','it','you','of','tinyurl.com','for','on','my','\'s','that','at','with','me','do']
            
    def BuildApiClient(self):
        auth = tweepy.OAuthHandler(secrets.twitterApiKey, secrets.twitterApiSecret)
        auth.set_access_token(secrets.twitterAccessToken, secrets.twitterAccessTokenSecret)
        return tweepy.API(auth)

    def StartSampleStream(self, streamListener, maxTweets):        
        api = self.BuildApiClient()
        myStream = tweepy.Stream(auth = api.auth, listener=streamListener)
        myStream.sample()        
        return

    def StartFilteredStream(self, streamListener, terms):
        api = self.BuildApiClient()
        myStream = tweepy.Stream(auth = api.auth, listener=streamListener)
        
        if len(terms == 0):
            # Use a few of the top words to get a set of tweets
            terms = self.topTerms[0:3]

        myStream.filter(track=terms, languages=["en"])
        return

stream = StreamBuilder()
StreamListener = MyStreamListener()
stream.StartSampleStream(StreamListener, 1)
