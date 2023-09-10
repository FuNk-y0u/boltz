
# [⚡]Boltz v-0.1!

Boltz is a free and open source spotify to mp3 converter api!
Its a api based on [spotify_dl](https://github.com/SathyaBhat/spotify-dl). Boltz uses heavily customized and modified version of [spotify_dl](https://github.com/SathyaBhat/spotify-dl).

## Documentation

To use [⚡]Boltz api simply:


# 1. configure boltz in config.py 
```python
    
# Your Spotify Client Tokens
CLIENT_ID = '[YOUR TOKEN HERE]'
CLIENT_SECRET = '[YOUR TOKEN HERE]'

# Your Download Location
DOWNLOAD_FOLDER = 'downloads/'
```

# 2.Example app using boltz:

```python

from src.boltz import * # import boltz

if __name__ == '__main__':
    bolt = boltz() # initialize boltz
    bolt.download("[SPOTIFY SHARE LINK]") # downloading pl
    
```

# 3. to run your app:
```bash
  $ python app.py 
```

## Dependencies
* Python 3
* Spotipy
* yt_dlp
* ffmpeg

## Acknowledgments
* [spotify_dl](https://github.com/SathyaBhat/spotify-dl)

