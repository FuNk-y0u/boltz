from src.imports import *
from src.boltzUtil import *
from src.constants import VERSION, DOWNLOADS_FOLDER
from src.spotify_dl import *

'''
Generates File System For Song Download
'''
def generateFilesystem( generateSeperatefolder):
    if(generateSeperatefolder == True):
        try:
            boltzUtil.logHeader("Attempting to generate file system")
            os.mkdir(DOWNLOADS_FOLDER)
            logHeader("Sucessfully created file system")
        except Exception as e:
            logError("Failed to create downloads folder")
    else:
        pass

'''
Download Playlist Function
'''

def downloadPl( playListlink, isZip, token):
    playListlink = playListlink
    isZip = isZip
    generateFilesystem(True)
    spotify_dl(playListlink, token)


    
if __name__ == '__main__':
    downloadPl('https://open.spotify.com/playlist/2y0Epzc7sqZGf8aDXGxZTx?si=6d166e8969574bed',False)


            



