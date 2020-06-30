import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import configparser

config = configparser.ConfigParser()
config.read('config.cfg')
client_id = config.get('SPOTIFY', 'CLIENT_ID')
client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
print(client_id)

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print('need username')
        sys.exit()
    
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        print()
        print(playlist['name'])
        print ('  total tracks', playlist['tracks']['total'])
        results = sp.playlist(playlist['id'],
            fields="tracks,next")
        tracks = results['tracks']
        show_tracks(tracks)
        while tracks['next']:
            tracks = sp.next(tracks)
            show_tracks(tracks)