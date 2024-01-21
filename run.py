import sys
import os

path = os.getcwd() + "/src"
sys.path.append(path)
path = os.getcwd() + "/boltz_api"
sys.path.append(path)

import src.main
