import collections

class IndexBuilder:
    
    def __init__(self):
        # TODO: Replace with build()
        self.Index = self.buildTest()
        
    def build(self):

        raise NotImplementedError() 
        return 

    ###
    # Temporary method to load a sample format for test purposes
    def buildTest(self):
        index = { 
            'appl': ['https://t.co/DAigxMguwz', 'https://t.co/YYSYYkZtFE'],
            'banana': ['https://t.co/DAigxMguwz', 'https://t.co/BCPj26VQIy'],
            'cherri': ['https://t.co/YYSYYkZtFE'],
            'date': ['https://t.co/BCPj26VQIy']
        }
        return index