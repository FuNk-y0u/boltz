import threading
import secrets

from flask import*
from flask_cors import CORS
from serverconfig import *

from src.boltz import *


app = Flask(__name__)
CORS(app)

def progressAdddef():
    file_data = None

    with open("user_progress.json","r") as json_file:
        file_data = json.load(json_file)
        json_file.close()

    with open("user_progress.json","w") as json_file:
        token = secrets.token_hex(8)
        detail = {"total_progress": 0, "current_song": "Null", "current_song_progress":0,"is_complete": False}
        file_data.update({token:detail})
        json.dump(file_data,json_file)
        json_file.close()
    return token

@app.route('/get', methods= ['POST'])
def example_route():
    token = request.data
    token = token.decode()
    token = token.replace('"','')
    with open("user_progress.json","r") as json_file:
        file_data = json.load(json_file)
        json_file.close()
    tprogress = file_data[token]["total_progress"]
    csong = file_data[token]["current_song"]
    iscomplete = file_data[token]["is_complete"]

    data = {
        "total_progress": str(tprogress),
        "current_song": csong,
        "is_complete": iscomplete,
    }
    return jsonify(data)

@app.route('/')
def home():
    link = str(request.args.get("linkBox"))
    if(link.startswith('https://open.spotify.com/')):
        file_token = progressAdddef()
        thread = threading.Thread(target=downloadPl, args=(link, False, file_token,))
        thread.start()
        return redirect(url_for("download_page", Token = file_token))
    else:
        return render_template("upload.html")

@app.route('/<Token>')
def download_page(Token):
    return render_template("download.html",file_token = Token, server_ip = SERVER_LINK)

@app.route('/download/<token>')
def download_zip(token):
    return send_file(f"{DOWNLOADS_FOLDER}/{token}/{token}.zip")

@app.route('/search')
def search():
    keywords = str(request.args.get("linkBox"))
    search_type = str(request.args.get("type"))
    results = spotify_search(keywords, search_type)
    if(str(results) == "None"):
        return render_template("search.html")
    else:
        return render_template("result.html", items = results, search_t = search_type, server_ip = SERVER_LINK)

@app.route('/res/<res>')
def result(res):
    res = res.split(',')
    link = 'https://open.spotify.com/' + res[0] + '/' + res[1]
    
    file_token = progressAdddef()
    thread = threading.Thread(target=downloadPl, args=(link, False, file_token,))
    thread.start()
    return redirect(url_for("download_page", Token = file_token))

    


    

if __name__ == '__main__':
    app.run(host=SERVER_IP, port=SERVER_PORT, debug=True)