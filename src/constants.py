'''
Constants For Api
'''
import os
from pathlib import Path

__all__ = ["VERSION"]
VERSION = "8.7.0"

if os.getenv("XDG_CACHE_HOME") is not None:
    SAVE_PATH = os.getenv("XDG_CACHE_HOME") + "/spotifydl"
else:
    SAVE_PATH = str(Path.home()) + "/.cache/spotifydl"

DOWNLOAD_LIST = "download_list.log"
DOWNLOADS_FOLDER = "./downloads"
CLIENT_ID = '0797e2fdf87b42ca8469beae2587bae4'
CLIENT_SECRET = '19fd3eb103e7482587c186b760b8f3c3'

