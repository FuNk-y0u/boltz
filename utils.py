
# ! File for all utilities for boltz

from models import *

# * Function to parse url to BoltzUrl
def parse_validate_url(url: str) -> [str,str]:
    _url = url

    if _url.startswith("https://open.spotify.com/"):
        try:
            _url = _url.replace("https://","")
            _url = _url.split("/")
            _type = _url[1]

            # [id]?[garbage], so removing garbage
            _id = _url[2].split("?")[0]

            return [_type, _id]
        
        except Exception as e:
            return [0,0]

    else:
        return [0,0]

# * Function to parse dict to BoltzItem
def parse_items(items:dict) -> list[BoltzItem]:

    _boltz_items = [] # list[BoltzItem]
    for item in items["items"]:

        _boltz_images = []
        _items_images = item["track"]["album"]["images"]

        if _items_images:
            for image in _items_images:
                _boltz_images.append(
                    BoltzImage(
                        image["width"],
                        image["height"],
                        image["url"]
                    )
                )
        
        _album_name =  item["track"]["album"]["name"] if item["track"]["album"]["name"] else ""
        _release_date = item["track"]["album"]["release_date"][:4] if item["track"]["album"]["name"] else ""
        _total_tracks = item["track"]["album"]["total_tracks"] if item["track"]["album"]["total_tracks"] else 0

        _boltz_artists = []
        _items_artists = item["track"]["artists"]
        if _items_artists:
            for artist in _items_artists:
                _boltz_artists.append(
                    BoltzArtist(
                        artist["name"],
                        artist["uri"]
                    )
                )
        
        _id = item["track"]["id"] if item["track"]["id"] else ""
        _name = item["track"]["name"] if item["track"]["name"] else ""
        _track_number = item["track"]["track_number"] if item["track"]["track_number"] else 0

        _boltz_items.append(BoltzItem(
            _boltz_images,
            _album_name,
            _release_date,
            _total_tracks,
            _boltz_artists,
            _id,
            _name,
            _track_number
        ))

    return _boltz_items # Returning list[BoltzItem]
