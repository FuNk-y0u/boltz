#!/usr/bin/env python3
import argparse
import time
import json
import os
import sys
import spotipy
import shutil

from pathlib import Path, PurePath
from spotipy.oauth2 import SpotifyClientCredentials

from src.boltzUtil import *
from src.constants import VERSION, DOWNLOADS_FOLDER, CLIENT_ID, CLIENT_SECRET

from src.spotify import (
    fetch_tracks,
    parse_spotify_url,
    validate_spotify_urls,
    get_item_name,
)

from src.youtube import download_songs, default_filename, playlist_num_filename


def spotify_dl(spotifyUrl, token):

    '''
    spotifyUrl: Url To Spotify Song / Album / Playlist
    token: Download Process Token
    '''

    spotifyUrl = spotifyUrl
    token = token
    num_cores = os.cpu_count()
    token = token

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=CLIENT_ID, client_secret=CLIENT_SECRET
        )
    )

    valid_urls = validate_spotify_urls(spotifyUrl)

    url_data = {"urls": []}
    for url in valid_urls:
        url_dict = {}

        item_type, item_id = parse_spotify_url(url)
        directory_name = get_item_name(sp, item_type, item_id)

        url_dict["save_path"] = Path(
            PurePath.joinpath(Path(DOWNLOADS_FOLDER +  "/"  + token + "/" ), Path(directory_name))
        )
        url_dict["save_path"].mkdir(parents=True, exist_ok=True)

        logHeader(
            f"Saving songs to {directory_name} directory"
        )

        url_dict["songs"] = fetch_tracks(sp, item_type, url, token)
        url_data["urls"].append(url_dict.copy())
        file_name_f = default_filename

        download_songs(token,
            songs=url_data,
            output_dir=DOWNLOADS_FOLDER +"/" + token + "/",
            file_name_f = file_name_f,
        )
        gen_zip(token)
        

def gen_zip(token):
    shutil.make_archive(f"{DOWNLOADS_FOLDER}/{token}/{token}", format='zip', root_dir = f"{DOWNLOADS_FOLDER}/{token}/")

def spotify_search(name, item_type):
    class item:
        track = 'track'
        playlist = 'playlist'
        album = 'album'

    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

    if(item_type == item.track):
        results = spotify.search(q=item.track+':' + name, type=item.track)
        items = results['tracks']['items']
        print("ITEMS LEN: " + str(len(items)))

        array_results = []
        for item in items:
            array_results.append({"name" : item['name'], "link":item['external_urls']['spotify'], "image":item['album']['images'][0]['url']})
        
        return array_results

    elif(item_type == item.album):
        results = spotify.search(q=item.album+':' + name, type=item.album)

        items = results['albums']['items']
        print("ITEMS LEN: " + str(len(items)))


        array_results = []
        for item in items:
            array_results.append({"name":item['name'], "link":item['external_urls']['spotify'], "image":item['images'][0]['url']})
        return array_results
    elif(item_type == item.playlist):
        
        results = spotify.search(q=item.playlist+':' + name, type=item.playlist)

        items = results['playlists']['items']
        print("ITEMS LEN: " + str(len(items)))


        array_results = []
        for item in items:
            array_results.append({"name":item['name'],"link":item['external_urls']['spotify'], "image":item['images'][0]['url']})
        return array_results





    
