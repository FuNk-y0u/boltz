from config import *
from sv_inc import *
from routes import *

app = fs.Flask(__name__)
fsc.CORS(app)

app.add_url_rule("/search", view_func = search, methods = ["POST"])

app.run(host = "127.0.0.1", port = 6969, debug = True)

