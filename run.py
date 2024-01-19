import sys
import os

path = os.getcwd() + "/src"
sys.path.append(path)
path += "/api"
sys.path.append(path)

import src.main
