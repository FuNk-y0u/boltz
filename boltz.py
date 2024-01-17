
# ! Main Boltz File
# TODO add search feature

from inc import *

class Boltz:

    # * Constructor
    def __init__(self, client_id:str, client_secret:str, save_path="./downloads") -> None:
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
        self.save_path = save_path

    # * Initializes and parses your url
    def initialize_url(self, _link:str) -> BoltzUrl:
        type, id = parse_validate_url(_link)

        if type != 0 and id != 0:
            return BoltzUrl(type, id, True)
        
        else:
            return BoltzUrl(type,id, False)
        
    # * conducts operation accoring to your link types
    def fetch_tracks(self, _boltzurl: BoltzUrl) -> list[BoltzTrack]:
        if _boltzurl.is_valid:

            match _boltzurl.type:
                case 'playlist':
                    tracks = self.__fetch_playlist(_boltzurl.id)
                    return tracks

                case 'album':
                   tracks = self.__fetch_album(_boltzurl.id)
                   return tracks

                case 'track':
                    track = self.__fetch_track(_boltzurl.id)
                    return [track]

                case _:
                    return []

    
    # * Fetches and parses playlist
    def __fetch_playlist(self, _id) -> list[BoltzTrack]:
        offset = 0 # Count for no of tracks

        _track_list = [] # List of BoltzTrack

        _is_running = True # For while loop below

        while _is_running:
            try:
                res_items = self.sp.playlist_items(
                    playlist_id= _id,
                    fields= SPOTIPY_FIELDS,
                    additional_types= ["track"],
                    offset= offset
                )
            except Exception as e:
                break
            
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
                    artists
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

    # * Fetches and parses album
    def __fetch_album(self, _id) -> list[BoltzTrack]:
        offset = 0 # count for no of tracks

        _track_list = []

        _is_running = True

        while _is_running:
            try:
                album_items = self.sp.album(album_id=_id)
                res_items = self.sp.album_tracks(album_id=_id, offset=offset)
            except Exception as e:
                break


            _total_songs = res_items.get("total")

            album = parse_album(album_items) # Parsing dict to BoltzAlbum

            main_artist_id = album.artists[0].uri

            genres = self.sp.artist(artist_id=main_artist_id).get("genres",[]) if main_artist_id else [] # Getting artist genre

            _items_parsed = parse_items_album(res_items, album) # Pasing dict to BoltzItem

            for item in _items_parsed:
                if item is None:
                    offset += 1
                    continue
            
                _track = BoltzTrack(item.id,
                            item.name,
                            item.track_number,
                            album,
                            ",".join([artist.name for artist in album.artists]),
                            genres[0] if genres else ""
                )

                _track_list.append(_track)

                offset += 1

            _is_running = False if _total_songs == offset else True # Checks if all the songs are processed

        return _track_list # Returning List[BoltzTrack]

    # * Fetches and parses track
    def __fetch_track(self, _id) -> BoltzTrack:
        try:
            res_items = self.sp.track(track_id=_id)
        except Exception as e:
            return []

        album = parse_album(res_items["album"])

        main_artist_id = album.artists[0].uri
        genres = self.sp.artist(artist_id=main_artist_id).get("genres",[]) if main_artist_id else [] # Getting artist genre

        _item_parsed = parse_item_track(res_items,album)

        _track = BoltzTrack(_item_parsed.id,
                            _item_parsed.name,
                            _item_parsed.track_number,
                            album,
                            ",".join([artist.name for artist in album.artists]),
                            genres[0] if genres else ""
        )

        return _track # Returning BoltzTrack

    # * Download and convert tracks
    def download_track(self, track:BoltzTrack) -> BoltzMP3:

        _query = generate_ytdl_query(track.artist, track.name)

        _filename = [f"{track.artist} - {track.name}", track.position]
        _filepath = path.join(self.save_path, _filename[0])

        mp3_filename = f"{_filepath}.mp3"

        _out_template = f"{_filepath}.%(ext)s"

        _yt_dl_options= generate_ytdl_opts(_out_template,
                                            SPONSOR_BLOCK_PP,
                                            track.name,
                                            track.artist,
                                            track.album
        )

        with yt_dlp.YoutubeDL(_yt_dl_options) as _ydl:
            try:
                _ydl.download([_query])
            
            except Exception as e:
                return BoltzMP3(False, track, mp3_filename, track.position)
            
            return BoltzMP3(True, track, mp3_filename, track.position)
    
    # * Adding details to song
    def set_tags(self, boltzmp3:BoltzMP3, _total_tracks:int) -> bool:
        try:
            mp3_file = MP3(boltzmp3.mp3_filename, ID3=EasyID3)
        except Exception as e:
            return False
        
        mp3_file["date"] = boltzmp3.track.album.year
        mp3_file["tracknumber"] = (str(boltzmp3.track.position) + "/" + str(_total_tracks))
        mp3_file["genre"] = boltzmp3.track.genre

        try:
            mp3_file.save()
        except Exception as e:
            return False

        mp3_file = MP3(boltzmp3.mp3_filename, ID3=ID3)
        cover = boltzmp3.track.album.cover

        if cover.lower().startswith("http"):
            try:
                _req = urllib.request.Request(cover)
                with urllib.request.urlopen(_req) as _response:
                    mp3_file.tags["APIC"] = APIC(
                        encoding=3,
                        mime="image/jpeg",
                        type=3,
                        desc="Front Cover",
                        data=_response.read(),
                    )
            except Exception as e:
                pass
        
        try:
            mp3_file.save()
            return True
        except Exception as e:
            return False

        
        