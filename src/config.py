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

CONFIG
'''


# Your Spotify Client Tokens
CLIENT_ID = '0797e2fdf87b42ca8469beae2587bae4'
CLIENT_SECRET = '19fd3eb103e7482587c186b760b8f3c3'

# Your Download Location
DOWNLOAD_FOLDER = 'downloads/'

#your zip output location
ZIP_LOCATION = './zips/'

# Use All The Cores Of your Computer to download songs at maximum speeds, can cause glitches
USE_FULL_CORE = True

# No of parallel downloads per time
# !NOTE only usable when USE_FULL_CORE is disabled
threshval = 5 

# deletion time for each zip file stored in seconds
DELETE_TIME = 18000

# checking time for deleting file
CHECK_TIME = 300