import os
import psutil

from config import*
from util import*

def main():
    pyutil = util()
    pyutil.log_info(" INSTALLING REQ DEPENDENCIES ")
    os.system("pip install spotify_dl")
    os.system("pip install youtube_dl")
    os.system("pip install django")
    os.system("pip install psutil")
    pyutil.log_info(" PLEASE INSTALL FFMPEG FROM RESPECTIVE APP STORE OF UR OS")
    pyutil.log_info(" SETTING IDS ")

    parent_pid = os.getppid()
    if("powershell" instr(psutil.Process(parent_pid).name())):
        os.system("")



    os.chdir()

if __name__ == "__main__":
    main()