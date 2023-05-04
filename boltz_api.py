import os
import threading
import shutil

from util import *
from config import *


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
        else:
        # Starting Download Thread
            self.download_thread = threading.Thread(target = self.download_thread, args=(playListlink,self.isZip,self.current_id))
            self.download_thread.start()

    def download_thread(self, link, c_zip, c_id):
        self.c_id = c_id
        self.link = link
        self.c_zip = c_zip
        try:
            self.pyutil.log_warning("Attempting to download songs from " + self.playListlink)

            # updating id file
            self.current_id = self.current_id + 1
            id_file = open("temp/current_id.txt", "w")
            id_file.write(str(self.current_id))
            id_file.close()

            # downloading using spotify_dl
            os.system(f'spotify_dl -l "{self.link}" -o {TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER}{str(self.c_id)}/')

            if(c_zip):
                shutil.make_archive(f"{TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER}zips/{str(self.c_id)}", format='zip', root_dir = f"{TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER}{str(self.c_id)}/")




            self.pyutil.log_ok("Sucessfully downloaded")


        except Exception as e:
            self.pyutil.log_warning("couldnot download playlist")
            self.pyutil.display_error(str(e))
            return 0

if __name__ == '__main__':
   boltz = spotify_download_api()
   boltz.download_pl("https://open.spotify.com/playlist/2y0Epzc7sqZGf8aDXGxZTx?si=7e1ccfda5574470d", True)

