from sv_inc    import *
from sv_models import *
from config    import *
from routes    import *

# Creating download root directory
if not os.path.exists(DOWNLOAD_ROOT):
	os.mkdir(DOWNLOAD_ROOT)

app = fs.Flask(__name__)
fsc.CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config[DOWNLOAD_PROGRESS] = {}
app.config["APP"] = app

with app.app_context():
	pdb.init_app(app)
	pdb.create_all()

app.add_url_rule("/search", view_func = search, methods = ["POST"])
app.add_url_rule("/download", view_func = download, methods = ["POST"])
app.add_url_rule("/get_status", view_func = get_status, methods = ["POST"])
app.add_url_rule("/get_file/<pl_id>", view_func = get_file, methods = ["GET"])

app.run(host = SV_IP, port = SV_PORT, debug = True)

