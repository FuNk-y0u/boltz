'''
▀█████████▄   ▄██████▄   ▄█           ███      ▄███████▄  
  ███    ███ ███    ███ ███       ▀█████████▄ ██▀     ▄██ 
  ███    ███ ███    ███ ███          ▀███▀▀██       ▄███▀ 
 ▄███▄▄▄██▀  ███    ███ ███           ███   ▀  ▀█▀▄███▀▄▄ 
▀▀███▀▀▀██▄  ███    ███ ███           ███       ▄███▀   ▀ 
  ███    ██▄ ███    ███ ███           ███     ▄███▀       
  ███    ███ ███    ███ ███▌    ▄     ███     ███▄     ▄█ 
▄█████████▀   ▀██████▀  █████▄▄██    ▄████▀    ▀████████▀   v0.2
                        ▀                                 
boltz was possible only due to spotify_dl,
https://github.com/SathyaBhat/spotify-dl,
please fork and star this repo thanks <3
'''

import argparse
import time
import json
import os
import sys
import spotipy
import shutil
import yt_dlp
import urllib.request
import multiprocessing

from pathlib import Path, PurePath
from spotipy.oauth2 import SpotifyClientCredentials

from src.const import CLIENT_ID, CLIENT_SECRET, DOWNLOAD_FOLDER
from src.boltz_util import *

from os import path
from mutagen.easyid3 import EasyID3
from mutagen.id3 import APIC, ID3
from mutagen.mp3 import MP3



class spItem():
    def __init__(self, itemName:str, itemType:str, itemId:str, itemSavepath:str ,itemSongs:str, totalSongs:int):
        self.itemName = itemName
        self.itemSongs = itemSongs
        self.itemSavepath = itemSavepath
        self.itemType = itemType
        self.itemId = itemId
        self.totalSongs = totalSongs

        self.progress = 0.0
        self.isCompleted = False
        self.downloadingSongs = []


class boltz:
    def __init__(self, CLIENT_ID = CLIENT_ID, CLIENT_SECRET = CLIENT_SECRET) -> None:

        '''
        [*] CLIENT_ID, CLIENT_SECRET -> spotify client tokens
        '''

        '''
        creates and returns spotify client
        '''
        self.spClient = self.create_sp_client(CLIENT_ID, CLIENT_SECRET)
    
    def download(self,url:str):

        if self.is_valid_url(url) == True:

            itemType, itemId = self.parse_url(url)
            itemName = self.get_item_name(self.spClient, itemType, itemId)
            downloadFolder = Path(PurePath.joinpath(Path(DOWNLOAD_FOLDER), Path(itemName)))

            itemSongs, totalSongs = self.fetch_tracks(self.spClient, itemType, url)

            item = spItem(itemName, itemType, itemId, Path(downloadFolder), itemSongs, totalSongs)

            downloadFolder.mkdir(parents=True, exist_ok=True)
            
            logHeader(f"saving songs to {downloadFolder}")

            self.find_download(item)

    def set_tags(self,spItem, filename, index):
        try:
            song_file = MP3(filename, ID3=EasyID3)
        except mutagen.MutagenError as e:
            displayError(e)
            logError(
                f"Failed to download: {filename}, please ensure YouTubeDL is up-to-date. "
            )

            return
        song_file["date"] = spItem.itemSongs[index - 1]["year"]
        song_file["tracknumber"] = (str(index) + "/" + str(spItem.totalSongs))
        song_file["genre"] = spItem.itemSongs[index - 1]["genre"]
        song_file.save()


        song_file = MP3(filename, ID3=ID3)
        cover = spItem.itemSongs[index -1]["cover"]
        if cover is not None:
            if cover.lower().startswith("http"):
                req = urllib.request.Request(cover)
            else:
                raise ValueError from None
            with urllib.request.urlopen(req) as resp:  # nosec
                song_file.tags["APIC"] = APIC(
                    encoding=3,
                    mime="image/jpeg",
                    type=3,
                    desc="Cover",
                    data=resp.read(),
                )
        song_file.save()

    def find_download(self, spItem):
        for song in spItem.itemSongs:
            

            name = song['name']
            artist = song['artist']
            album = song['album']
            index = 1

            query = f"{artist} - {name} Lyrics".replace(":","").replace('"',"")
            fileName = f"{artist} - {name}", index
            filePath = path.join(spItem.itemSavepath, fileName[0])
            mp3FileName = f"{filePath}.mp3"
            mp3FilePath = path.join(mp3FileName)

            sponsorblockPostprocessor = [
                    {
                        "key": "SponsorBlock",
                        "categories": ["skip_non_music_sections"],
                    },
                    {
                        "key": "ModifyChapters",
                        "remove_sponsor_segments": ["music_offtopic"],
                        "force_keyframes": True,
                    },
            ]
            outtmpl = f"{filePath}.%(ext)s"
            ydlOpts = {
                "quiet":True,
                "proxy": "",
                "default_search": "ytsearch",
                "format": "bestaudio/best",
                "outtmpl": outtmpl,
                "postprocessors": sponsorblockPostprocessor,
                "noplaylist": True,
                "no_color": False,
                "postprocessor_args": [
                    "-metadata",
                    "title=" + name,
                    "-metadata",
                    "artist=" + artist,
                    "-metadata",
                    "album=" + album,
                ],
            }
            mp3PostprocessOpts = {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
            ydlOpts["postprocessors"].append(mp3PostprocessOpts.copy())


            with yt_dlp.YoutubeDL(ydlOpts) as ydl:
                try:
                    ydl.download([query])
                    
                except Exception as e:  # skipcq: PYL-W0703
                    displayError(e)
                    displayError(f"Failed to download {name}, make sure yt_dlp is up to date")
            self.set_tags(spItem, mp3FileName, index)
            index += 1



    def fetch_tracks(self, sp, item_type:str, url:str):
        songs_list = []
        offset = 0
        songs_fetched = 0
        total_songs = 0

        if item_type == "playlist":
            while True:
                
                items = sp.playlist_items(
                    playlist_id=url,
                    fields="items.track.name,items.track.artists(name, uri),"
                    "items.track.album(name, release_date, total_tracks, images),"
                    "items.track.track_number,total, next,offset,"
                    "items.track.id",
                    additional_types=["track"],
                    offset=offset,
                )
                total_songs = items.get("total")
                for item in items["items"]:
                    track_info = item.get("track")
                    # If the user has a podcast in their playlist, there will be no track
                    # Without this conditional, the program will fail later on when the metadata is fetched
                    if track_info is None:
                        offset += 1
                        continue
                    track_album_info = track_info.get("album")
                    track_num = track_info.get("track_number")
                    spotify_id = track_info.get("id")
                    track_name = track_info.get("name")
                    track_artist = ",".join(
                        [artist["name"] for artist in track_info.get("artists")]
                    )
                    if track_album_info:
                        track_album = track_album_info.get("name")
                        track_year = (
                            track_album_info.get("release_date")[:4]
                            if track_album_info.get("release_date")
                            else ""
                        )
                        album_total = track_album_info.get("total_tracks")
                    if len(item["track"]["album"]["images"]) > 0:
                        cover = item["track"]["album"]["images"][0]["url"]
                    else:
                        cover = None
                    artists = track_info.get("artists")
                    main_artist_id = (
                        artists[0].get("uri", None) if len(artists) > 0 else None
                    )
                    genres = (
                        sp.artist(artist_id=main_artist_id).get("genres", [])
                        if main_artist_id
                        else []
                    )
                    if len(genres) > 0:
                        genre = genres[0]
                    else:
                        genre = ""
                    songs_list.append(
                        {
                            "name": track_name,
                            "artist": track_artist,
                            "album": track_album,
                            "year": track_year,
                            "num_tracks": album_total,
                            "num": track_num,
                            "playlist_num": offset + 1,
                            "cover": cover,
                            "genre": genre,
                            "spotify_id": spotify_id,
                            "track_url": None,
                        }
                    )
                    offset += 1
                    songs_fetched += 1

                if total_songs == offset:
                    break

        elif item_type == "album":
            while True:
                album_info = sp.album(album_id=url)
                items = sp.album_tracks(album_id=url, offset=offset)
                total_songs = items.get("total")
                track_album = album_info.get("name")
                track_year = (
                    album_info.get("release_date")[:4]
                    if album_info.get("release_date")
                    else ""
                )
                album_total = album_info.get("total_tracks")
                
                if len(album_info["images"]) > 0:
                    cover = album_info["images"][0]["url"]
                else:
                    cover = None
                if (
                    len(sp.artist(artist_id=album_info["artists"][0]["uri"])["genres"])
                    > 0
                ):
                    genre = sp.artist(artist_id=album_info["artists"][0]["uri"])[
                        "genres"
                    ][0]
                else:
                    genre = ""
                for item in items["items"]:
                    track_name = item.get("name")
                    track_artist = ", ".join(
                        [artist["name"] for artist in item["artists"]]
                    )
                    track_num = item["track_number"]
                    spotify_id = item.get("id")
                    songs_list.append(
                        {
                            "name": track_name,
                            "artist": track_artist,
                            "album": track_album,
                            "year": track_year,
                            "num_tracks": album_total,
                            "num": track_num,
                            "track_url": None,
                            "playlist_num": offset + 1,
                            "cover": cover,
                            "genre": genre,
                            "spotify_id": spotify_id,
                        }
                    )
                    offset += 1
                if album_total == offset:
                    break
        elif item_type == "track":
            items = sp.track(track_id=url)
            track_name = items.get("name")
            album_info = items.get("album")
            track_artist = ", ".join([artist["name"] for artist in items["artists"]])
            if album_info:
                track_album = album_info.get("name")
                track_year = (
                    album_info.get("release_date")[:4]
                    if album_info.get("release_date")
                    else ""
                )
                album_total = album_info.get("total_tracks")
            track_num = items["track_number"]
            spotify_id = items["id"]

            if len(items["album"]["images"]) > 0:
                cover = items["album"]["images"][0]["url"]
            else:
                cover = None
            if len(sp.artist(artist_id=items["artists"][0]["uri"])["genres"]) > 0:
                genre = sp.artist(artist_id=items["artists"][0]["uri"])["genres"][0]
            else:
                genre = ""
            songs_list.append(
                {
                    "name": track_name,
                    "artist": track_artist,
                    "album": track_album,
                    "year": track_year,
                    "num_tracks": album_total,
                    "num": track_num,
                    "playlist_num": offset + 1,
                    "cover": cover,
                    "genre": genre,
                    "track_url": None,
                    "spotify_id": spotify_id,
                }
            )

        return songs_list, total_songs
        



    def get_item_name(self,spClient, itemType, itemId):
        if itemType == "playlist":
            name = spClient.playlist(playlist_id=itemId, fields="name").get("name")
        elif itemType == "album":
            name = sp.album(album_id=itemId).get("name")
        elif itemType == "track":
            name = sp.track(track_id=itemId).get("name")
        return self.sanitize(name)
    
    def sanitize(self,name, replace_with=""):
        clean_up_list = ["\\", "/", ":", "*", "?", '"', "<", ">", "|", "\0", "$", "\""]
        for x in clean_up_list:
            name = name.replace(x, replace_with)
        return name

    
    def is_valid_url(self,url:str) -> bool:

        itemType, itemId = self.parse_url(url)

        if itemType not in ["album", "track", "playlist"]:

            logHeader(f"Only albums/tracks/playlists are supported and not {itemType}")
            return False

        if itemId is None:

            logError(f"Couln't get valid item id for {url}")
            return False
        else:
            return True
    
    
    def parse_url(self,url:str) -> str:

        if url.startswith("spotify:"):

            logError("Spotify URI was provided instead of a playlist/album/track URL.")
            sys.exit(-1)

        elif url.startswith("https://open.spotify.com/"):

            parsedUrl = url.replace("https://open.spotify.com/", "").split("?")[0]
            itemType = parsedUrl.split("/")[0]
            itemId = parsedUrl.split("/")[1]
            return itemType, itemId
        else:

            logError("Invalid Url")
            return "ERROR", "ERROR"

    def create_sp_client(self,clientId:str, clientSecret:str):
        '''
        [*] clientId, clientSecret -> spotify client tokens
        '''
        try:

            __spotifyClient = spotipy.Spotify(
                auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
                )
            logHeader("Sucessfully created spotify client")
            return __spotifyClient

        except Exception as e:

            logError("Unable To Create Spotify Client")
            displayError(e)
            sys.exit(-1)


    


