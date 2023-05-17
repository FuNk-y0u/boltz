import threading
import secrets

from flask import*
from flask_cors import CORS
from serverconfig import *

from src.boltz import *


app = Flask(__name__)
CORS(app)

'''

! parses token from client

'''
def parse_token(data):
    data = data.decode()
    data = data.replace('"','')
    return data


'''

! generates default value for client and generates token

'''
def progress_add_def():
    fileData = None

    with open("user_progress.json","r") as jsonFile:
        fileData = json.load(jsonFile)
        jsonFile.close()

    with open("user_progress.json","w") as jsonFile:
        
        # generating file token 
        token = secrets.token_hex(8)

        detail = {"total_progress": 0, "current_song": "Null", "current_song_progress":0,"is_complete": False}
        fileData.update({token:detail})
        json.dump(fileData,jsonFile)
        jsonFile.close()

    return token


'''

! used for progress updating

'''
@app.route('/get', methods= ['POST'])
def progress_route():

    # parsing token from client
    token = parse_token(request.data)

    with open("user_progress.json","r") as jsonFile:
        fileData = json.load(jsonFile)
        jsonFile.close()
    
    '''

    * totalProgress = Total progress of conversion in %
    * currentSong = current song being converted
    * isComplete = true or false when the total conversion is completed

    '''

    totalProgress = fileData[token]["total_progress"]
    currentSong = fileData[token]["current_song"]
    isComplete = fileData[token]["is_complete"]

    data = {
        "total_progress": str(totalProgress),
        "current_song": currentSong,
        "is_complete": isComplete,
    }

    return jsonify(data)


'''

! for home screen

'''
@app.route('/')
def home():

    '''
    * link = spotify playlist link
    * fileToken = token generated for each conversion
    '''

    link = str(request.args.get("linkBox"))

    # checking if link provided is valid
    if(link.startswith('https://open.spotify.com/')):

        fileToken = progress_add_def()

        conversionThread = threading.Thread(target=downloadPl, args=(link, fileToken,))
        conversionThread.start()

        return redirect(url_for("download_page", token = fileToken))
    else:
        return render_template("upload.html")


'''

! for download page

'''
@app.route('/<token>')
def download_page(token):
    return render_template("download.html",file_token = token, server_ip = SERVER_LINK)

'''

! provides file to the client when redirected

'''
@app.route('/download/<token>')
def download_zip(token):
    return send_file(f"{DOWNLOADS_FOLDER}/{token}/{token}.zip")

'''

! for search page

'''
@app.route('/search')
def search():
    '''

    * keyWords = search text
    * searchType = which to search for, either album, track or playlist
    * results = list of dict full of results and data

    '''

    keyWords = str(request.args.get("linkBox"))
    searchType = str(request.args.get("type"))

    # searching for the results
    results = spotify_search(keyWords, searchType)

    # checking if there is no result
    if(str(results) == "None"):
        
        return render_template("search.html")
    else:

        return render_template("result.html", results = results, search_type = searchType, server_ip = SERVER_LINK)

'''
! for redirecting to conversion page
'''

@app.route('/res/<raw>')
def result(raw):

    # parsing and generating spotify link
    raw = raw.split(',')
    link = 'https://open.spotify.com/' + raw[0] + '/' + raw[1]
    
    fileToken = progress_add_def()

    conversionThread = threading.Thread(target=downloadPl, args=(link, fileToken,))
    conversionThread.start()

    return redirect(url_for("download_page", token = fileToken))


'''

! runs server on execution

'''
if __name__ == '__main__':
    app.run(host=SERVER_IP, port=SERVER_PORT, debug=True)