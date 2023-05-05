import os
import threading
import shutil
import json

from src.util import *
from src.config import *

from src.spotify_dl import spotify_dl
import sys
import os

os.environ["SPOTIPY_CLIENT_ID"] = '0797e2fdf87b42ca8469beae2587bae4'
os.environ["SPOTIPY_CLIENT_SECRET"] = '19fd3eb103e7482587c186b760b8f3c3'

class spotify_download_api:
    def initialize(self):
        self.pyutil = util()
        self.current_id = 0


    def generate_folder(self):

        #folder generation and id stuff
        try:
            self.pyutil.log_warning("Attempting To Create New 'temp' folder")
            os.mkdir(TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER)
            self.pyutil.log_ok("Sucessfully Created 'temp' folder in " + TEMP_FOLDER_LOCATION)
            id_file = open("temp/current_id.txt", "w")
            id_file.write("0")
            id_file.close()
            pass
        except Exception as e:
            self.pyutil.log_warning("couldnot create 'temp/' because it exists or something went wrong")
            self.pyutil.display_error(str(e))
            self.pyutil.log_warning("reading from current_id.txt")
            id_file = open("temp/current_id.txt", "r")
            self.current_id = id_file.readlines()
            self.current_id = int(self.current_id[0])
            id_file.close()
            pass


    def __init__(self):

        #initialization stuff
        self.initialize()
        self.generate_folder()

        
    def download_pl(self, playListlink, isZip):
        
        self.playListlink = playListlink
        self.isZip = isZip

        # checking for validity of playlist
        self.pyutil.log_warning("checking for validity of link")
        if(not (self.playListlink.startswith('https://open.spotify.com/playlist/'))):
            self.pyutil.log_error("sorry invalid link!")
            return "invlink"
        else:
        # Starting Download Thread
            try:
                self.pyutil.log_warning("Attempting to download songs from " + self.playListlink)

                # updating id file
                self.current_id = self.current_id + 1
                id_file = open("temp/current_id.txt", "w")
                id_file.write(str(self.current_id))
                id_file.close()

                sys.argv.append("-l")
                sys.argv.append(self.playListlink)
                sys.argv.append("-o")
                sys.argv.append(f'{TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER}{str(self.current_id)}/')
                spotify_dl.spotify_dl()


                if(self.isZip):
                    shutil.make_archive(f"{TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER}zips/{str(self.current_id)}", format='zip', root_dir = f"{TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER}{str(self.current_id)}/")
                    shutil.rmtree(f"{TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER}{str(self.current_id)}/")
                    return (str(self.current_id))

                self.pyutil.log_ok("Sucessfully downloaded")


            except Exception as e:
                self.pyutil.log_warning("couldnot download playlist")
                self.pyutil.display_error(str(e))
        

if __name__ == '__main__':
    config = json.load(open("config.json", "r"))
    urls = config["playlist_url"]
    iszip = config["zip"]

    boltz = spotify_download_api()
    for url in urls:
        boltz.pyutil.log_warning("Downloading " + url + " ... " )
        boltz.download_pl(url, iszip)

