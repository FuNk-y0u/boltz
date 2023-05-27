
# [⚡]Boltz v-0.1!

Its a api based on [spotify_dl](https://github.com/SathyaBhat/spotify-dl). Boltz uses highly customized and modified version of [spotify_dl](https://github.com/SathyaBhat/spotify-dl) specificly built for boltz website [boltz](https://bolz.herokuapp.com).


## Usage

To use [⚡]Boltz api simply:


1. in "config.py" 
```python
    
# Your Spotify Client Tokens
CLIENT_ID = '[YOUR TOKEN HERE]'
CLIENT_SECRET = '[YOUR TOKEN HERE]'

# Your Download Location
DOWNLOAD_FOLDER = 'downloads/'

# Use All The Cores Of your Computer to download songs at maximum speeds, can cause glitches
USE_FULL_CORE = True

# No of parallel downloads per time
# !NOTE only usable when USE_FULL_CORE is disabled
threshval = 5 
```
2. in bash
```bash
  $ python app.py 
```
    
## Example

```python

from src.boltz import * # import boltz

if __name__ == '__main__':
    bolt = boltz() # initialize boltz
    bolt.download("https://open.spotify.com/playlist/0XS5MxyJ7x8jqveJoG7K8N?si=090c5aa164634117") # downloading pl
    
```

