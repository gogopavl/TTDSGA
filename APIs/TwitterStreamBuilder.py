import tweepy
import secrets
from TwitterStreamListener import TwitterStreamListener

class TwitterStreamBuilder():
    # From http://techland.time.com/2009/06/08/the-500-most-frequently-used-words-on-twitter/
    topTerms = ['the','i','to','a','and','is','in','it','you','of','tinyurl.com','for','on','my','\'s','that','at','with','me','do']
            
    def BuildApiClient(self):
        auth = tweepy.OAuthHandler(secrets.twitterApiKey, secrets.twitterApiSecret)
        auth.set_access_token(secrets.twitterAccessToken, secrets.twitterAccessTokenSecret)
        return tweepy.API(auth)

    def StartSampleStream(self, maxTweets):        
        api = self.BuildApiClient()
        streamListener = TwitterStreamListener(api, maxTweets)        
        myStream = tweepy.Stream(auth = api.auth, listener=streamListener)
        myStream.sample()        
        return

    def StartFilteredStream(self, maxTweets, terms):
        api = self.BuildApiClient()
        streamListener = TwitterStreamListener(api, maxTweets)
        myStream = tweepy.Stream(auth = api.auth, listener=streamListener)
        
        if len(terms) == 0:
            # Use a few of the top words to get a set of tweets
            terms = self.topTerms[0:3]

        myStream.filter(track=terms, languages=["en"])
        return
