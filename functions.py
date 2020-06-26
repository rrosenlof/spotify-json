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
THUMBNAILS_PER_ROW = 8
THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 300
MODE = 'RGB'

# prints the play count from a json file of streaming history
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

# prints some info from json file of latest listening history in a csv-type format
def get_latest():
    with open("json/latest-6-12-20.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        for p in data['items']:
            print("{},{},{},\n".format(p['artists'][0]['name'],p['name'] ,p['popularity']))

# gets list of artwork urls from json file of a playlist
def get_artwork():
    with open("json/2020-playlist.json", encoding="utf8") as json_file:
        data = json.load(json_file)
        artworks = []
        for p in data['items']:
            artworks.append(p['track']['album']['images'][1]['url'])

        artworks = list(dict.fromkeys(artworks))    

        return artworks

# makes a jpg collage from a list of urls, using constants defined above
def make_collage(artworks):
    artworks = sort_artwork(artworks)
    
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

# sorts the artworks based on hsv data
def sort_artwork(artworks):
    listArtColors = []
    reps = len(artworks)
    for artwork in artworks:
        fd = urlopen(artwork)
        f = io.BytesIO(fd.read())
        color = ColorThief(f)            
        dominant_color = color.get_color(quality=1)
        hsv_color = step(dominant_color[0], dominant_color[1], dominant_color[2],300 )
        dictArtColors = dict(artwork=artwork, color=hsv_color)
        listArtColors.append(dictArtColors)
        print(dictArtColors['color'][0])
    
    listArtColors.sort(key=lambda x: x['color'][0])

    return listArtColors

# changes color from rgb to hsv
def format_color(rgb_color):
    return colorsys.rgb_to_hsv(rgb_color[0], rgb_color[1], rgb_color[2])

# changes color to custom hsv value
def step(r,g,b, repetitions=1):
    lum = math.sqrt(.241*r + .691*g + .068*b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)

    return (h2,lum,v2)
