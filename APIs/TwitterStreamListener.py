import sys, time, json
import tweepy
from collections import namedtuple
from Tweet import Tweet
from MSVision import GetImageResults
from  index_collection import index_collection


class TwitterStreamListener(tweepy.StreamListener):
    _maxTweets = 1
    _tweetCount = 0
    
    def __init__(self, api=None, maxTweets=1):
        self._maxTweets = maxTweets
        self._tweetCount = 0
        super().__init__(api=api)
        #instantiate
        self._db = index_collection()
        
    def on_status(self, status):      
        media = self.get_media(status)
        if media is None:
            return

        self._tweetCount += 1

        tweet = Tweet()
        tweet.Text = status.text
        tweet.Url = media["url"]
        tweet.ImageUrl = media["media_url_https"]
        
        # print("***** TWEET #{0} *****".format(self._tweetCount))
        # print(tweet.Text)
        # print(tweet.ImageUrl)
        # print(tweet.Url)
        
        # Call vision API
        vision_json = GetImageResults(tweet.ImageUrl)
        vision = json.loads(vision_json, object_hook=lambda obj: namedtuple('result', obj.keys())(*obj.values()))

        tweetjson = status._json
        tweetID = tweetjson["id"] # Retrieve tweet id
        
        # Combine wanted tweet info and vision api output together
        tweetAndVision = {}
        tweetAndVision["Tweet"] = {"ID" : tweetID, "Text" : tweet.Text, "URL" : tweet.Url} # What about hashtags?
        tweetAndVision["VisionResults"] = json.loads(vision_json)
        print(json.dumps(tweetAndVision)) # Print for now - Will be passed to the II Module
        
        # Display to console for now
        # print("***** VISION RESULTS *****")
        # print("Tags:")
        # for tag in vision.tags:
        #     print("{0:.00%} : {1}".format(tag.confidence, tag.name))
        # print("Captions")
        # for caption in vision.description.captions:
        #     print("{0:.00%} : {1}".format(caption.confidence, caption.text))

        # print("\n")
        # Check count to limit utilization while in development
        
        #update DB
        self._db.update(tweetAndVision)


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
