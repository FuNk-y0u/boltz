
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
        _release_year = item["track"]["album"]["release_date"][:4] if item["track"]["album"]["name"] else ""
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
            _release_year,
            _total_tracks,
            _boltz_artists,
            _id,
            _name,
            _track_number
        ))

    return _boltz_items # Returning list[BoltzItem]

# * Function to parse dict to BoltzAlbum
def parse_album(album_info:dict) -> BoltzAlbum:

    _album_name = album_info["name"] if album_info["name"] else ""
    _release_year = album_info["release_date"][:4] if album_info["release_date"] else ""
    _total_tracks = album_info["total_tracks"] if album_info["total_tracks"] else 0

    _album_images = album_info["images"]
    _boltz_images = []
    if _album_images:
        for image in _album_images:
            _boltz_images.append(
                BoltzImage(
                    image["width"],
                    image["height"],
                    image["url"]
                )
            )
    
    _boltz_artists = []
    _album_artists = album_info["artists"]

    if _album_artists:
        for artist in _album_artists:
            _boltz_artists.append(
                BoltzArtist(
                    artist["name"],
                    artist["uri"]
                )
            )
    
    return BoltzAlbum(
        _album_name,
        _release_year,
        _total_tracks,
        _boltz_images[0].url if _boltz_images[0] else None,
        _boltz_artists
    )

# * Function to parse dict to BoltzItems with album       
def parse_items_album(items:dict, album:BoltzAlbum) -> list[BoltzItem]:
    _boltz_items = [] # list[BoltzItem]
    for item in items["items"]:
        _items_image = album.cover
        
        _album_name =  album.name
        _release_year = album.year
        _total_tracks = album.total_tracks

        _boltz_artists = []
        _items_artists = item["artists"]
        if _items_artists:
            for artist in _items_artists:
                _boltz_artists.append(
                    BoltzArtist(
                        artist["name"],
                        artist["uri"]
                    )
                )
        
        _id = item["id"] if item["id"] else ""
        _name = item["name"] if item["name"] else ""
        _track_number = item["track_number"] if item["track_number"] else 0

        _boltz_items.append(BoltzItem(
            [_items_image],
            _album_name,
            _release_year,
            _total_tracks,
            _boltz_artists,
            _id,
            _name,
            _track_number
        ))

    return _boltz_items # Returning list[BoltzItem]

# * Function to parse dict to BoltzItem
def parse_item_track(item:dict, album:BoltzAlbum) -> BoltzItem:
    _boltz_item = None # list[BoltzItem]
    
    _items_image = album.cover
    
    _album_name =  album.name
    _release_year = album.year
    _total_tracks = album.total_tracks

    _boltz_artists = []
    _items_artists = item["artists"]
    if _items_artists:
        for artist in _items_artists:
            _boltz_artists.append(
                BoltzArtist(
                    artist["name"],
                    artist["uri"]
                )
            )
    
    _id = item["id"] if item["id"] else ""
    _name = item["name"] if item["name"] else ""
    _track_number = item["track_number"] if item["track_number"] else 0

    _boltz_item = BoltzItem(
        [_items_image],
        _album_name,
        _release_year,
        _total_tracks,
        _boltz_artists,
        _id,
        _name,
        _track_number
    )

    return _boltz_item # Returning list[BoltzItem]

def generate_ytdl_query(_artist:str, _song_name:str) -> str:
    _query = f"{_artist} - {_song_name} Lyrics"
    _query = _query.replace(':','').replace(' " ', '') # removing unwanted characters in query
    return _query

def generate_ytdl_opts(_out_template:str,
                       _post_processor:[dict],
                       _track_name:str,
                       _track_artist:str,
                       _track_album:str) -> dict:
    
    _ytdl_opts = {
        "quiet":True,
        "proxy": "",
        "default_search": "ytsearch",
        "format": "bestaudio/best",
        "outtmpl": _out_template,
        "postprocessors": [],
        "noplaylist": True,
        "no_color": False,
        "postprocessor_args": [
            "-metadata",
            "title=" + _track_name,
            "-metadata",
            "artist=" + _track_artist,
            "-metadata",
            "album=" + _track_album.name,
        ],
    }

    mp3_pp_opts = {
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }

    _ytdl_opts["postprocessors"].append(mp3_pp_opts.copy())

    return _ytdl_opts

# * Parses and returns link of results
def parse_search_res(items:dict, type:str) -> [BoltzSearchResult]:

    items = items[type + 's']
    items = items["items"]

    _search_res = []

    for item in items:

        _type = item["type"] 
        _id = item["id"]

        _title = item["name"] if item["name"] else "Unknown"

        if(type != BoltzSearchTypes.playlist):
            _artist = item["artists"][0]["name"] if item["artists"][0]["name"]  else "Unknown"
        else:
            _artist = item["owner"]["display_name"]

        if(type == BoltzSearchTypes.track):
            _image = item["album"]["images"][0]
            _image = BoltzImage(_image["width"],_image["height"],_image["url"])
        else:
            _image = item["images"][0]
            _image = BoltzImage(_image["width"],_image["height"],_image["url"])
        
        _search_res.append(
            BoltzSearchResult(
                BoltzUrl(_type, _id, True),
                _title,
                _artist,
                _image
            )
        )
    return _search_res
        

        


def ASSERT(_condition:bool, _message:str):
    if(not _condition):
        print(_message)
        exit()
    
    

