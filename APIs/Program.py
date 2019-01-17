from TwitterStreamBuilder import TwitterStreamBuilder
from TwitterStreamListener import TwitterStreamListener
from MS_Vision import getImageResults

def TestTwitterAndVIsionApi():
    ### Stream will shut down once maxTweets have been received    
    maxTweets = 3
    stream = TwitterStreamBuilder()

    # Continuous stream of sampled tweets
    stream.StartSampleStream(maxTweets)

    # Tweets matching targeted terms
    #stream.StartFilteredStream(maxTweets, ["brexit"])

def TestVisionApi():
    urlImage = 'https://media.wired.com/photos/5b86fce8900cb57bbfd1e7ee/master/pass/Jaguar_I-PACE_S_Indus-Silver_065.jpg'
    results = getImageResults(urlImage)
    print(results)


TestTwitterAndVIsionApi()
#TestVisionApi()