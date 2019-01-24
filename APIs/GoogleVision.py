from google.cloud import vision

def detect_logos_uri(uri):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.logo_detection(image=image)
    logos = response.logo_annotations
    print('Logos:')

    for logo in logos:
        print(logo.description)

urlImage = 'https://fm.cnbc.com/applications/cnbc.com/resources/img/editorial/2018/11/07/105559579-1541619188419rts24ng1.530x298.jpg?v=1541619280'
detect_logos_uri(urlImage)