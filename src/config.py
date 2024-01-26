from sv_inc import *

load_dotenv()

CLIENT_ID     = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

DOWNLOAD_ROOT = "./downloads/"   # NOTE: Dont forget to add ending slash
DOWNLOAD_PROGRESS = "DOWNLOAD_PROGRESS"
