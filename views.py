
import email
import io
import os
import urllib.parse
import uuid
from werkzeug.utils import secure_filename
from unicodedata import name
from warnings import catch_warnings
from flask import Flask, Response, redirect,render_template, request,session,jsonify, url_for
from jinja2 import Template
import base64
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_mail import Mail
from sqlalchemy.exc import IntegrityError 
# from flask_ngrok import run_with_ngrok
from __init__ import app,db
from models import *

with open('config.json',"r") as c:
    params=json.load(c)['params']

@app.route("/",methods=["GET","POST","PUT","DELETE","HEAD"])
def index():
    song_id = Songs.get_random_song_id()
    song_id="9047c1b666"
    
    return redirect(url_for('playsong', song_id=song_id))
    
    # random_song_id = Songs.get_random_song_id()

    # # return render_template("indexmob.html",params=params)
    # return render_template("player.html" ,song_id=random_song_id)
@app.route("/play")
def playsong():
    song_id = request.args.get('song_id')
    action=request.args.get('action')
    current_song=Songs.query.get(song_id)
    pageTitle="Home"
    if action and current_song:
        
        if action=="prev":
            previous_song_id = current_song.get_previous_song_id()
            return redirect(url_for('playsong', song_id=previous_song_id))
            
        if action=="next":
            next_song_id = current_song.get_next_song_id()
            return redirect(url_for('playsong', song_id=next_song_id))
        
    if current_song is None:
        song_id = Songs.get_random_song_id()
        # print(song_id)
    if song_id:
        song = Songs.query.get(song_id)
        pageTitle=song.songName
        
    
        
    # return render_template("indexmob.html",params=params)
    return render_template("player.html" ,
                           song_id=song_id,
                           pageTitle=pageTitle,
                           )

@app.route("/mob",methods=["GET","POST","PUT","DELETE","HEAD"])
def indexmob():
    return render_template("indexmob.html",params=params)



# @app.route("/xyz-account" ,methods=["GET","POST","PUT","DELETE","HEAD"])
# def account():
#     if (request.method=='POST'):
#         # songname=request.form.get("songname") 
#         # songlyrics=request.form.get("songlyrics")
#         artist=request.form.get("artist")
#         songName=request.form.get("songname")
#         album=request.form.get("album")  
#         userid=request.form.get("userid")  
#         date=request.form.get("date")
#         app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['uploadSong'])
#         f=request.files["filesongaudio"]
#         f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
#         app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['uploadLyrics'])
#         #app.config['UPLOAD_FOLDER']=params['uploadLyrics']
#         g=request.files["filesonglyrics"]
#         g.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(g.filename)))
#         app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['uploadBg'])
#         h=request.files["filesongbg"]
#         h.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(h.filename)))
#         songEntry=Songs(songName=songName,songAudio=secure_filename(f.filename),songBg=secure_filename(h.filename),songLyrics=secure_filename(g.filename),songAlbum=album ,songArtist=artist,uploadId=userid,date=datetime.now())
#         db.session.add(songEntry)
#         db.session.commit()   
        
#     return render_template("account.html")


@app.route("/xyz-account", methods=["GET", "POST", "PUT", "DELETE", "HEAD"])
def account():
    if request.method == 'POST':
        artist = request.form.get("artist")
        songName = request.form.get("songname")
        album = request.form.get("album")
        userid = request.form.get("userid")
        date = datetime.now()

        # Process and store the uploaded files as BLOBs
        filesongaudio = request.files.get("filesongaudio").read()
        filesonglyrics = request.files.get("filesonglyrics").read()
        filesongbg = request.files.get("filesongbg").read()
        songId=uuid.uuid4().hex[:10]

        songEntry = Songs(
            songId=songId,
            songName=songName,
            songArtist=artist,
            songAlbum=album,
            uploadId=userid,
            date=date,
            songLyrics=filesonglyrics,  # Store lyrics as BLOB
            songBg=filesongbg,  # Store background as BLOB
            songAudio=filesongaudio  # Store audio file data as BLOB
        )

        db.session.add(songEntry)
        db.session.commit()

    return render_template("account.html")

# @app.route("/get-songs", methods=["GET"])
# def get_songs():
#     songs = Songs.query.all()
    
#     song_list = []

#     for song in songs:
#         # Encode song lyrics and background as base64
#         song_lyrics_base64 = base64.b64encode(song.songLyrics).decode('utf-8')
#         song_bg_base64 = base64.b64encode(song.songBg).decode('utf-8')

#         # Create a data URI for the audio
#         song_audio_data_uri = f"data:audio/mp3;base64,{base64.b64encode(song.songAudio).decode('utf-8')}"

#         song_data = {
#             "id": song.songId,
#             "songName": song.songName,
#             "songArtist": song.songArtist,
#             "songAlbum": song.songAlbum,
#             "uploadId": song.uploadId,
#             "date": song.date.strftime("%Y-%m-%d %H:%M:%S"),
#             "songLyrics": song_lyrics_base64,
#             "songBg": song_bg_base64,
#             "songAudio": song_audio_data_uri,
#             # You can add other fields as needed
#         }

#         song_list.append(song_data)

#     return jsonify(songs=song_list)

@app.route("/get-songs", methods=["GET"])
def get_songs():
    songs = Songs.query.all()
    
    song_list = []

    for song in songs:
        # Encode song lyrics and background as base64
        song_lyrics_base64 = base64.b64encode(song.songLyrics).decode('utf-8')
        song_bg_base64 = base64.b64encode(song.songBg).decode('utf-8')

        # Create a data URI for the audio
        song_audio_data_uri = f"data:audio/mp3;base64,{base64.b64encode(song.songAudio).decode('utf-8')}"

        song_data = {
            "id": song.songId,
            "songName": song.songName,
            "songArtist": song.songArtist,
            "songAlbum": song.songAlbum,
            "uploadId": song.uploadId,
            "date": song.date.strftime("%Y-%m-%d %H:%M:%S"),
            "songLyrics": song_lyrics_base64,
            "songBg": song_bg_base64,
            "songAudio": song_audio_data_uri,
            # You can add other fields as needed
        }

        song_list.append(song_data)

    return jsonify(songs=song_list)


@app.route("/get-song/<string:song_id>", methods=["GET"])
def get_song_by_id(song_id):
    song = Songs.query.get(song_id)

    if song:
        song_data = {
            "songId": song.songId,  # Change 'id' to 'songId'
            "songName": song.songName,
            "songArtist": song.songArtist,
            "songAlbum": song.songAlbum,
            "uploadId": song.uploadId,
            "date": song.date.strftime("%Y-%m-%d %H:%M:%S"),
        }

        # You can add other fields as needed

        return jsonify(song=song_data)
    else:
        return jsonify(error="Song not found"), 404

# Add routes to download original files
@app.route("/download/song-lyrics/<string:song_id>", methods=["GET"])
def download_song_lyrics(song_id):
    song = Songs.query.get(song_id)

    if song:
        return Response(io.BytesIO(song.songLyrics), content_type="text/plain")
    else:
        return jsonify(error="Song not found"), 404

@app.route("/download/song-bg/<string:song_id>", methods=["GET"])
def download_song_bg(song_id):
    song = Songs.query.get(song_id)

    if song:
        return Response(io.BytesIO(song.songBg), content_type="video/mp4")
    else:
        return jsonify(error="Song not found"), 404

@app.route("/download/song-audio/<string:song_id>", methods=["GET"])
def download_song_audio(song_id):
    song = Songs.query.get(song_id)

    if song:
        return Response(io.BytesIO(song.songAudio), content_type="audio/mpeg")
    else:
        return jsonify(error="Song not found"), 404


# @app.route("/get-song/<string:song_id>", methods=["GET"])
# def get_song_by_id(song_id):
#     song = Songs.query.get(song_id)

#     if song:
#         # Encode song lyrics and background as base64
#         song_lyrics_base64 = base64.b64encode(song.songLyrics).decode('utf-8')
#         song_bg_base64 = base64.b64encode(song.songBg).decode('utf-8')

#         # Create a data URI for the audio
#         song_audio_data_uri = f"data:audio/mp3;base64,{base64.b64encode(song.songAudio).decode('utf-8')}"

#         song_data = {
#             "id": song.songId,
#             "songName": song.songName,
#             "songArtist": song.songArtist,
#             "songAlbum": song.songAlbum,
#             "uploadId": song.uploadId,
#             "date": song.date.strftime("%Y-%m-%d %H:%M:%S"),
#             "songLyrics": song_lyrics_base64,
#             "songBg": song_bg_base64,
#             "songAudio": song_audio_data_uri,
#             # You can add other fields as needed
#         }

#         return jsonify(song=song_data)
#     else:
#         return jsonify(error="Song not found"), 404


@app.route("/loader")
def loader():
    return render_template("loader.html")

@app.context_processor
def default():
    user=0
    favsong=[]
    
    cred=Songs.query.all()
    #cred=cred[2].songName
    return dict(cred=cred,fav=favsong)
