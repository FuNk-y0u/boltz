
# [⚡]Boltz v-0.2!

Boltz is a free and open source spotify to mp3 converter api and website!
[WEBSITE] for online conversion (uses boltz v-0.1) : [boltz](https://bolz.herokuapp.com)

Its a api based on [spotify_dl](https://github.com/SathyaBhat/spotify-dl). Boltz uses heavily customized and modified version of [spotify_dl](https://github.com/SathyaBhat/spotify-dl) specificly built for boltz website [boltz](https://bolz.herokuapp.com).


## Documentation

To use [⚡]Boltz api simply:


## 1. configure boltz in config.py 
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

## 2.Example app using boltz:

```python

from src.boltz import * # import boltz

if __name__ == '__main__':
    bolt = boltz() # initialize boltz
    bolt.download("[SPOTIFY SHARE LINK]") # downloading pl
    
```

## 3. to run your app:
```bash
  $ python app.py 
```
    

