#!/usr/bin/python
import json
from PIL import Image
import requests
from io import BytesIO
import math
from colorthief import ColorThief

THUMBNAILS_PER_ROW = 6
THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 300
MODE = 'RGB'

def get_data():
    count = 0
    with open("json/StreamingHistory0.json",  encoding="utf8") as json_file:
        data = json.load(json_file)
        for p in data:
            if p['msPlayed'] > 0:
                print(p['trackName'])
                count += 1
        print('----------')
        print("Play count: {0}".format(count))

def get_latest():
    with open("json/latest-6-12-20-short_term.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        for p in data['items']:
            print("{},{},{}".format(p['artists'][0]['name'],p['name'] ,p['popularity']))

def get_artwork():
    with open("json/latest-6-12-20-short_term.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        artworks = []
        for p in data['items']:
            artworks.append(p['album']['images'][1]['url'])

        artworks = list(dict.fromkeys(artworks))    

        return artworks

def make_collage(artworks):

    extra = len(artworks) % THUMBNAILS_PER_ROW

    while (extra > 0):
        artworks.pop()
        extra -= 1
    
    width = THUMBNAIL_WIDTH*THUMBNAILS_PER_ROW if len(artworks)>=THUMBNAILS_PER_ROW else THUMBNAILS_PER_ROW*len(artworks)
    height = math.ceil(len(artworks)/THUMBNAILS_PER_ROW)*THUMBNAIL_HEIGHT
    rgb_image = Image.new(MODE, (width,height), color=0)

    counter = 0
    for artwork in artworks:
        response = requests.get(artwork)
        img = Image.open(BytesIO(response.content))
        img = img.convert(MODE)

        pos_right = (counter % THUMBNAILS_PER_ROW) * THUMBNAIL_WIDTH
        pos_down = (counter//THUMBNAILS_PER_ROW)*THUMBNAIL_HEIGHT
        rgb_image.paste(img,(pos_right,pos_down), mask=None)
        counter += 1

    rgb_image.save('collage.jpg')


            


                