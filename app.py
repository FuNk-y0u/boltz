'''
▀█████████▄   ▄██████▄   ▄█           ███      ▄███████▄  
  ███    ███ ███    ███ ███       ▀█████████▄ ██▀     ▄██ 
  ███    ███ ███    ███ ███          ▀███▀▀██       ▄███▀ 
 ▄███▄▄▄██▀  ███    ███ ███           ███   ▀  ▀█▀▄███▀▄▄ 
▀▀███▀▀▀██▄  ███    ███ ███           ███       ▄███▀   ▀ 
  ███    ██▄ ███    ███ ███           ███     ▄███▀       
  ███    ███ ███    ███ ███▌    ▄     ███     ███▄     ▄█ 
▄█████████▀   ▀██████▀  █████▄▄██    ▄████▀    ▀████████▀   v0.2
                        ▀                                 
boltz was possible only due to spotify_dl,
https://github.com/SathyaBhat/spotify-dl,
'''

from src.boltz import *
from flask import*
from server_config import *
from src.boltz import *
from src.config import ZIP_LOCATION
from src.cleanup import *

from flask_cors import CORS
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import secrets
import threading
import shutil

bolt = boltz()

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
bolt_db = SQLAlchemy(app)

class item(bolt_db.Model):
  id  = bolt_db.Column(bolt_db.Integer, primary_key=True)
  Name = bolt_db.Column(bolt_db.String(50))
  Type = bolt_db.Column(bolt_db.String(50))
  itemSid = bolt_db.Column(bolt_db.String(50))
  Path = bolt_db.Column(bolt_db.String(100))
  Progress = bolt_db.Column(bolt_db.String(10), default="0")
  Total =bolt_db.Column(bolt_db.String(10), default="0")
  boltId = bolt_db.Column(bolt_db.String(50))
  isCompleted = bolt_db.Column(bolt_db.Boolean, default=False)
  timeOfGen = bolt_db.Column(bolt_db.Integer, default=round(time.time()))
  isDisabled = bolt_db.Column(bolt_db.Boolean, default=False)
  Songs = bolt_db.relationship('song', backref='item')


class song(bolt_db.Model):
  id  = bolt_db.Column(bolt_db.Integer, primary_key=True)
  itemId = bolt_db.Column(bolt_db.Integer, bolt_db.ForeignKey('item.id'))
  Name = bolt_db.Column(bolt_db.String(100))
  Artist = bolt_db.Column(bolt_db.String(50))
  Album = bolt_db.Column(bolt_db.String(50))
  Year = bolt_db.Column(bolt_db.String(50))
  Cover = bolt_db.Column(bolt_db.String(1000))
  Genre = bolt_db.Column(bolt_db.String(100))
  trackSid = bolt_db.Column(bolt_db.String(50))
  Status = bolt_db.Column(bolt_db.String(50), default="PENDING")

cleanup_thread= threading.Thread(target=clean_up, args=(item,song,bolt_db,app))

@app.route('/', methods=['POST'])
def upload():
  response = request.get_json()
  url = response['link']

  if bolt.is_valid_url(url) == True:
    itemType, itemId = bolt.parse_url(url)
    itemName = bolt.get_item_name(bolt.spClient, itemType, itemId)
    conversionToken = secrets.token_hex(8)
    downloadFolder = Path(PurePath.joinpath(Path(DOWNLOAD_FOLDER), Path(conversionToken)))
    itemSongs, totalSongs = bolt.fetch_tracks(bolt.spClient, itemType, url)

    
    
    spotifyItem = item(Name = itemName, Type = itemType, itemSid = itemId, Path=downloadFolder.__str__(), Total = totalSongs, boltId=conversionToken)
    bolt_db.session.add(spotifyItem)
    bolt_db.session.commit()

    for track in itemSongs:
      spotifyTrack = song(itemId = spotifyItem.id, Name=track['name'],Artist=track['artist'],Album=track['album'],Year=track['year'], Cover=track['cover'], Genre=track['genre'],trackSid=track['spotify_id'])
      bolt_db.session.add(spotifyTrack)
    bolt_db.session.commit()

    downloadFolder.mkdir(parents=True, exist_ok=True)
    logHeader(f"saving songs to {downloadFolder}")

    conversionThread = threading.Thread(target=bolt.find_download, args=(item,song,bolt_db,app, conversionToken,))
    conversionThread.start()
    
    tmpResp = {"token": conversionToken}
    return jsonify(tmpResp)




@app.route('/<token>', methods=['POST'])
def req(token):
  spotifyItem = item.query.filter_by(boltId=token).first()
  spotifySongs = song.query.filter_by(itemId = spotifyItem.id).all()

  response = {
    "Name":spotifyItem.Name,
    "Type":spotifyItem.Type,
    "Progress": spotifyItem.Progress,
    "boltId": spotifyItem.boltId,
    "isCompleted": spotifyItem.isCompleted,
    "songs": [],
  }
  for track in spotifySongs:
    song_detail = {
      "Name": track.Name,
      "Artist": track.Artist,
      "Album": track.Album,
      "Year": track.Year,
      "Genre": track.Genre,
      "Status": track.Status,
    }
    response["songs"].append(song_detail)
  
  return jsonify(response)

@app.route('/download/<token>')
def download(token):
  return send_file(f'{ZIP_LOCATION}{token}.zip')






if __name__ == '__main__':
  cleanup_thread.start()
  app.run(host=SERVER_IP, port=PORT, debug=True)
  cleanup_thread.join()
