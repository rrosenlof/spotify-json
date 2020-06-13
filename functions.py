#!/usr/bin/python
import json
from PIL import Image
import requests
from io import BytesIO
import io
import math
from colorthief import ColorThief
import sys
from urllib.request import urlopen
import colorsys

# Constants
THUMBNAILS_PER_ROW = 4
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
    with open("json/latest-6-12-20.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        for p in data['items']:
            print("{},{},{}".format(p['artists'][0]['name'],p['name'] ,p['popularity']))

def get_artwork():
    with open("json/2020-playlist.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        artworks = []
        # for p in data['items']:
        #     artworks.append(p['album']['images'][1]['url'])
        for p in data['items']:
            artworks.append(p['track']['album']['images'][1]['url'])

        artworks = list(dict.fromkeys(artworks))    

        return artworks

def make_collage(artworks):

    artworks = sort_artwork(artworks)

    # extra = len(artworks) % THUMBNAILS_PER_ROW

    # while (extra > 0):
    #     artworks.pop()
    #     extra -= 1
    
    width = THUMBNAIL_WIDTH*THUMBNAILS_PER_ROW if len(artworks)>=THUMBNAILS_PER_ROW else THUMBNAILS_PER_ROW*len(artworks)
    height = math.ceil(len(artworks)/THUMBNAILS_PER_ROW)*THUMBNAIL_HEIGHT
    rgb_image = Image.new(MODE, (width,height), color=0)

    counter = 0
    for artwork in artworks:
        response = requests.get(artwork['artwork'])
        img = Image.open(BytesIO(response.content))
        img = img.convert(MODE)

        pos_right = (counter % THUMBNAILS_PER_ROW) * THUMBNAIL_WIDTH
        pos_down = (counter//THUMBNAILS_PER_ROW)*THUMBNAIL_HEIGHT
        rgb_image.paste(img,(pos_right,pos_down), mask=None)
        counter += 1

    rgb_image.save('images/collage-2020-1.jpg')

def sort_artwork(artworks):
    listArtColors = []
    for artwork in artworks:
        fd = urlopen(artwork)
        f = io.BytesIO(fd.read())
        color = ColorThief(f)            
        dominant_color = color.get_color(quality=1)
        hsv_color = step(dominant_color[0], dominant_color[1], dominant_color[2], 8)
        dictArtColors = dict(artwork=artwork, color=hsv_color)
        listArtColors.append(dictArtColors)
    
    # listArtColors.sort(key=lambda x: x['color'][1], reverse=True)
    # listArtColors.sort(key=lambda x: x['color'], reverse=True)
    listArtColors.sort(key=lambda x: x['color'][1])

    return listArtColors

def format_color(rgb_color):
    return colorsys.rgb_to_hsv(rgb_color[0], rgb_color[1], rgb_color[2])
    # return math.sqrt(.241*math.pow(rgb_color[0],2) + .691*math.pow(rgb_color[1],2) + .068*math.pow(rgb_color[2],2))

def step(r,g,b, repetitions=1):
    lum = math.sqrt(.241*r + .691*g + .068*b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)

    return (h2,lum,v2)
