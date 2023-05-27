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
CLIENT_ID = ''
CLIENT_SECRET = ''

# Your Download Location
DOWNLOAD_FOLDER = 'downloads/'

# Use All The Cores Of your Computer to download songs at maximum speeds, can cause glitches
USE_FULL_CORE = True

# No of parallel downloads per time
# !NOTE only usable when USE_FULL_CORE is disabled
threshval = 5 