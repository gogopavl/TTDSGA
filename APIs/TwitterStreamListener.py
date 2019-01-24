import sys, time, json
import tweepy
from collections import namedtuple
from AnalysedTweet import AnalysedTweet
from MSVision import analyse_image
from  IndexCollection import IndexCollection


class TwitterStreamListener(tweepy.StreamListener):
    _maxTweets = 1
    _tweetCount = 0
    
    def __init__(self, api=None, maxTweets=1):
        self._maxTweets = maxTweets
        self._tweetCount = 0
        super().__init__(api=api)
        #instantiate
        self._db = IndexCollection()
        
    def on_status(self, status):      
        media = self.get_media(status)
        if media is None:
            return

        self._tweetCount += 1

        # Pass wanted data into analysed tweet instance
        atweet = AnalysedTweet()
        atweet.Id = status.id
        atweet.Text = status.text
        atweet.Url = media["url"]
        atweet.ImageUrl = media["media_url_https"]

        vision_json = analyse_image(atweet.ImageUrl)
        vision = json.loads(vision_json, object_hook=lambda obj: namedtuple('result', obj.keys())(*obj.values()))

        atweet.VisionResults = vision

        # Add tweet to index
        self._db.add_tweet(atweet)

        #update DB
        # self._db.update(tweetAndVision)

        # Check count to limit utilization while in development
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
