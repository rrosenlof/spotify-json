import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
import math
import requests
import configparser
from io import BytesIO
from flask.helpers import send_file

config = configparser.ConfigParser()
config.read('config.cfg')
client_id = config.get('SPOTIFY', 'CLIENT_ID')
client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def show_playlists(username):
    playlists = sp.user_playlists(username)
    return playlists

def get_tracks(username,playlist_id):
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def get_playlist(playlist_id):
    playlist = sp.playlist(playlist_id)
    return playlist

def make_collage(artworks, row, w):
    print(artworks)
    width = w*row if len(artworks)>=row else row*len(artworks)
    height = math.ceil(len(artworks)/row)*w
    rgb_image = Image.new('RGB', (width,height), color=0)

    counter = 0
    for artwork in artworks:
        response = requests.get(artwork)
        img = Image.open(BytesIO(response.content))
        img = img.convert('RGB')

        pos_right = (counter % row) * w
        pos_down = (counter//row)*w
        rgb_image.paste(img,(pos_right,pos_down), mask=None)
        counter += 1

    return rgb_image

def serve_image(img):
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')