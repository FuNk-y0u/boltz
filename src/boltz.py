import os

from src.boltzUtil import *
from src.constants import VERSION, DOWNLOADS_FOLDER
from src.spotify_dl import *

'''
Generates File System For Song Download
'''
def generate_file_system(generateSeperatefolder):
    if(generateSeperatefolder == True):
        try:
            logHeader("Attempting to generate file system")

            os.mkdir(DOWNLOADS_FOLDER)

            logHeader("Sucessfully created file system")

        except Exception as e:

            pass
    else:
        pass

'''
Download Playlist Function
'''

def downloadPl( playListlink, token):
    playListlink = playListlink
    generateFilesystem(True)
    spotify_dl(playListlink, token)





