from TwitterStreamBuilder import TwitterStreamBuilder
from TwitterStreamListener import TwitterStreamListener
from MSVision import GetImageResults

def TestTwitterAndVIsionApi():
    ### Stream will shut down once maxTweets have been received    
    maxTweets = 3
    stream = TwitterStreamBuilder()

    # Continuous stream of sampled tweets
    stream.StartSampleStream(maxTweets)

    # Tweets matching targeted terms
    #stream.StartFilteredStream(maxTweets, ["brexit"])

def TestVisionApi():
    # urlImage = 'https://media.wired.com/photos/5b86fce8900cb57bbfd1e7ee/master/pass/Jaguar_I-PACE_S_Indus-Silver_065.jpg'
    urlImage = 'https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2018/11/07/105559579-1541619188419rts24ng1.530x298.jpg?v=1541619280'
    results = GetImageResults(urlImage)
    print(results)


TestTwitterAndVIsionApi()
# TestVisionApi()
