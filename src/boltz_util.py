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

Utility For Boltz
'''

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def logHeader( text):
    print(colors.HEADER + "[BOLTZ INFO] " + text)
    
def logError( text):
    print(colors.FAIL + "[BOLTZ LOG] " + text)

def logOk( text):
    print(colors.OKGREEN + "[BOLTZ OK] " + text)
    
def displayError( text):
    print(colors.HEADER + "[ERROR CODE]")
    print(colors.FAIL + str(text))
    print(colors.HEADER + "~[ERROR CODE]")
