
# ! Main Boltz File
from inc import *

class Boltz:

    # * Constructor
    def __init__(self, client_id=CLIENT_ID, client_secret=CLIENT_SECRET) -> None:
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    # * Initializes and parses your url
    def initialize_url(self, _link:str) -> BoltzUrl:

        # TODO maybe merge the parse_validate_func here?
        type, id = parse_validate_url(_link)
        if type != 0 and id != 0:
            return BoltzUrl(type, id, True)
        
        else:
            return BoltzUrl(type,id, False)
        
    # * conducts operation accoring to your link types
    def fetch_tracks(self, _boltzurl: BoltzUrl) -> None:

        if _boltzurl.is_valid:
            match _boltzurl.type:

                case 'playlist':
                    tracks = self.__fetch_playlist(_boltzurl.id)

                case 'album':
                    print('album')

                case 'track':
                    print('track')

                case _:
                    print("Not supported by boltz")
    
    # * Fetches and parses playlist
    def __fetch_playlist(self, _id) -> list[BoltzTrack]:
        offset = 0 # Count for no of tracks

        _track_list = [] # List of BoltzTrack

        _is_running = True # For while loop below

        while _is_running:

            res_items = self.sp.playlist_items(
                playlist_id= _id,
                fields= SPOTIPY_FIELDS,
                additional_types= ["track"],
                offset= offset
            ) # Returns a dict
            
            res_items_parsed = parse_items(res_items) # Parsing dict to List[BoltzItem]

            _total_songs = res_items["total"] # Total tracks in the playlist

            for item in res_items_parsed:

                album_images = item.album_images
                artists = item.artists

                main_artist_id = artists[0].uri if artists else None

                genres = self.sp.artist(artist_id=main_artist_id).get("genres",[]) if main_artist_id else []


                if item is None:
                    offset += 1
                    continue
                
                _track_album = BoltzAlbum(
                    item.name,
                    item.release_date,
                    item.total_tracks,
                    album_images[0].url if album_images[0] else None,
                )

                _track = BoltzTrack(item.id,
                                    item.name,
                                    item.track_number,
                                    _track_album,
                                    ",".join([artist.name for artist in artists]),
                                    genres[0] if genres else ""
                )
                _track_list.append(_track)

                offset += 1

            _is_running = False if _total_songs == offset else True # Checks if all the songs are processed
        
        return _track_list # Returning list[BoltzItem]
    

if __name__ == "__main__":

    _boltzController = Boltz() # * Initializing boltz controller

    url = _boltzController.initialize_url("https://open.spotify.com/playlist/44koDbevdmaNIXhaWYkSHY?si=a6a8c0fa695b49c6") # * Passing in pl link

    if(url.is_valid): # Checks if the url is valid
        _boltzController.fetch_tracks(url) # * Fetches the info about tracks

    else:
        print("error invalid link") # ! Prints if the url is invalid