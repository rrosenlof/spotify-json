import sys
import spotipy
# import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

import configparser

config = configparser.ConfigParser()
config.read('config.cfg')
client_id = config.get('SPOTIFY', 'CLIENT_ID')
client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
print(client_id)

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

search_str = 'Muse'
result = sp.search(search_str)
print(result)