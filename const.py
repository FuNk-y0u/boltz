
# ! File for all boltz constants

# * Data needed from spotify api after fetching pl
SPOTIPY_FIELDS = ("items.track.name,items.track.artists(name, uri),"
"items.track.album(name, release_date, total_tracks, images),"
"items.track.track_number,total, next, offset,"
"items.track.id") 

# * YTDL filtering options
SPONSOR_BLOCK_PP = [
    {
        "key": "SponsorBlock",
        "categories": ["skip_non_music_sections"],
    },
    {
        "key": "ModifyChapters",
        "remove_sponsor_segments": ["music_offtopic"],
        "force_keyframes": True,
    },
]

# * Spotify Search Limit
SPOTIFY_SEARCH_LIMIT = 20
