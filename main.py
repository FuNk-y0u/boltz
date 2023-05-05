from flask import Flask, redirect, url_for, render_template, request, send_file
from src.boltz_api import *
from src.config import *
app = Flask(__name__)

@app.route("/")
def home():
    var = "robesckey"
    return render_template("index.html",  variable=var)

@app.route("/convert")
def convert():
    if request.method == "GET":
        link = request.args.get('pl_link')
        if(link != None):
            if(link.startswith('https://open.spotify.com/playlist/')):
                boltz = spotify_download_api()
                file_id = boltz.download_pl(str(link), True)
                if(file_id == "invlink"):
                    flash("Please Check Your Spotify Link And Try Again!")

                return redirect("thankyou/" + str(file_id))
        return render_template("convert.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/thankyou/<fileId>")
def thankyou(fileId):
    if request.method == "GET":
        fileid = request.args.get('file')
        if(fileid != None):
            filePath = TEMP_FOLDER_LOCATION + DOWNLOADS_FOLDER + "zips/" + str(fileid) + ".zip"
            try:
                return send_file(filePath, as_attachment=True)
            except:
                return redirect("/error")
        return render_template("thankyou.html",file_id=fileId, file_name = str(fileId) + ".zip")

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True)
