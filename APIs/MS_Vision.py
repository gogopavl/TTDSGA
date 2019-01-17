import time 
import requests
import operator
import json as JSON

_region = 'westeurope' 
_url = "https://{}.api.cognitive.microsoft.com/vision/v2.0/analyze".format(_region)
_key = "fed5d823105447a38a310a001b73dcd6"
_maxNumRetries = 2

def main():
    urlImage = 'https://media.wired.com/photos/5b86fce8900cb57bbfd1e7ee/master/pass/Jaguar_I-PACE_S_Indus-Silver_065.jpg'
    results = getImageResults(urlImage)
    print(results)

def getImageResults(urlImage):
    
    # API parameters for recognition found in:
    # https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fa
    params = { 'visualFeatures' : 'Description,Tags'}

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json'

    json = { 'url': urlImage } 
    data = None

    result = processRequest( json, data, headers, params )
    return JSON.dumps(result)


def processRequest( json, data, headers, params ):
    """
    Method to process requests to the API

    Parameters:
    json: Contains image url
    data: Set to none - used for image uploading
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        if response.status_code == 429: 
            print( "Message: %s" % ( response.json() ) )

            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
                if 'application/json' in response.headers['content-type'].lower(): 
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower(): 
                    result = response.content
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )

        break
        
    return result

#main()