# Boltz [⚡]
  
Boltz is a Python-based API simplifying Spotify playlist, album, and track conversion to MP3, allowing users to save music to their preferred location. Developers leverage Boltz to efficiently retrieve Spotify content by providing identifiers, utilizing Spotify's infrastructure for data fetching and MP3 conversion. Users specify the destination directory for flexibility in managing their library. Boltz streamlines Spotify access, empowering developers to innovate with music applications like players, backups, and playlist converters in Python projects.

## Index
1. [Install boltz](#How-to-install?)
2. [Use guide](#How-to-use?)
3. [Examples](#Wallah!)
## How to install?

 
 1. Clone the boltz repository

	```bash
	$ git clone https://github.com/FuNk-y0u/boltz/
	```
2. Get into the folder
	```bash
	$ cd boltz
	```
3. Install dependencies
	```bash
	$ pip install -r requirements.txt
	```
4. Install FFmpeg

	For windows:
	```powershell
	ps choco install ffmpeg
	```
	For linux:
	```bash
	$ sudo  apt  install ffmpeg
	```

## How to use?

1. Including boltz in your python file
```python
from inc import *
from boltz import *
```
2. Creating boltz controller
```python
_boltzController = Boltz(CLIENT_ID, CLIENT_SECRET, "[your download path]")
```
3. Initializing url
```python
url = _boltzController.initialize_url("[playlist url here]")
# Assert for error checking
ASSERT(url.is_valid, "Error: Spotify url is not valid")
```
4. Fetching tracks from playlist url
```python
tracks = _boltzController.fetch_tracks(url)
# Assert for error checking
ASSERT(tracks, "Error: while fetching tracks")
```
5. Looping through tracks obtained from playlist
```python
for track in tracks
```
6.  Downloading and converting + setting tags to mp3
```python
# * Looping through all the tracks in playlist/album/track
for track in tracks:
    print(f"Dowloading: {track.name} ...")

    # * Downloading track
    mp3 = _boltzController.download_track(track)

    # * Setting tags in mp3 file
    ASSERT(_boltzController.set_tags(mp3, len(tracks)), "Error: while converting to mp3")

    print(f"Downloaded: {track.name}")
```
## Wallah!
### code to download songs from playlist
```python
from inc import *
from boltz import *

# * Loading client_id and client_secret for boltz api
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# * Initializing boltz controller
_boltzController = Boltz(CLIENT_ID, CLIENT_SECRET, "[download path]")

# * Passing in pl link
url = _boltzController.initialize_url("[playlist url]")
ASSERT(url.is_valid, "Error: Spotify url is not valid")

tracks = _boltzController.fetch_tracks(url)
ASSERT(tracks, "Error: while fetching tracks")

# * Looping through all the tracks in playlist/album/track
for track in tracks:
    print(f"Dowloading: {track.name} ...")

    # * Downloading track
    mp3 = _boltzController.download_track(track)

    # * Setting tags in mp3 file
    ASSERT(_boltzController.set_tags(mp3, len(tracks)), "Error: while converting to mp3")

    print(f"Downloaded: {track.name}")
```
## Searching songs through Boltz api
```python
from boltz import *

# * Loading client_id and client_secret for boltz api
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Creating boltz controller
_boltzController = Boltz(CLIENT_ID, CLIENT_SECRET)

# Getting results of Phonk
results = _boltzController.search_song("Phonk",BoltzSearchTypes.playlist,50)

# Looping through each result
for result in results:
    print(result.title + ":" + result.url.id + ":" + str(result.image.url))
```
