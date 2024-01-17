from inc import *
from boltz import *

# * Loading client_id and client_secret for boltz api
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# * Initializing boltz controller
_boltzController = Boltz(CLIENT_ID, CLIENT_SECRET, "./downloads")

# * Passing in pl link
url = _boltzController.initialize_url("https://open.spotify.com/playlist/4WXsLmfw6PGuvHf12vrt7m?si=1bdbc59da60c4636")
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