from sv_utils import *

load_dotenv()

SV_IP = "127.0.0.1"
# SV_IP = socket.gethostbyname(socket.gethostname())
SV_PORT = 6969

CLIENT_ID     = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

DOWNLOAD_ROOT = "./downloads/"   # NOTE: Dont forget to add ending slash
DOWNLOAD_PROGRESS = "DOWNLOAD_PROGRESS"

# In bytes
# 1GB
MAX_DOWNLOAD_SIZE = 1000 * 1000 * 1000
