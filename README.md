
# [⚡]Boltz!

Its a api based on [spotify_dl](https://github.com/SathyaBhat/spotify-dl). Boltz uses highly customized and modified version of [spotify_dl](https://github.com/SathyaBhat/spotify-dl) specificly built for boltz website which is currently in development.


## Usage

To use [⚡]Boltz api simply:


1. in "config.json" 
```json
    {
    "playlist_url": [
        "your playlist link here",
        "your playlist link 2 here"
    ],
    
    "zip": true
}
```
2. in bash
```bash
  $ python bolz_api.py
```
    
## Example

```python
from boltz_api import *

boltz = spotify_download_api()
boltz.download_pl(sporitfy_url, zipsongs)
```

