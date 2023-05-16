import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = '0797e2fdf87b42ca8469beae2587bae4'
CLIENT_SECRET = '19fd3eb103e7482587c186b760b8f3c3'

class item:
    track = 'track'
    playlist = 'playlist'
    album = 'album'


spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
name = "counting stars"
item_type = item.track

if(item_type == item.track):
    results = spotify.search(q=item.track+':' + name, type=item.track)
    print(results)
    items = results['tracks']['items']
    print("ITEMS LEN: " + str(len(items)))

    for item in items:
        print(item['name'], item['external_urls']['spotify'], item['album']['images'][0]['url'])

elif(item_type == item.album):
    results = spotify.search(q=item.album+':' + name, type=item.album)

    items = results['albums']['items']
    print("ITEMS LEN: " + str(len(items)))

    for item in items:
        print(item['name'], item['external_urls']['spotify'], item['images'][0]['url'])

elif(item_type == item.playlist):
    results = spotify.search(q=item.playlist+':' + name, type=item.playlist)
    items = results['playlists']['items']
    print("ITEMS LEN: " + str(len(items)))

    for item in items:
        print(item['name'], item['external_urls']['spotify'], item['images'][0]['url'])





