from sv_inc import *
from config import *
from routes import *

# Creating download root directory
if not os.path.exists(DOWNLOAD_ROOT):
	os.mkdir(DOWNLOAD_ROOT)

app = fs.Flask(__name__)
fsc.CORS(app)

app.add_url_rule("/search", view_func = search, methods = ["POST"])
app.add_url_rule("/download", view_func = download, methods = ["POST"])
app.run(host = "127.0.0.1", port = 6969, debug = True)

