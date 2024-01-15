
# ! File for all boltz constants

# * Data needed from spotify api after fetching pl
SPOTIPY_FIELDS = ("items.track.name,items.track.artists(name, uri),"
"items.track.album(name, release_date, total_tracks, images),"
"items.track.track_number,total, next, offset,"
"items.track.id") 

# * Spotify Client Tokens
CLIENT_ID='0797e2fdf87b42ca8469beae2587bae4'
CLIENT_SECRET='19fd3eb103e7482587c186b760b8f3c3'