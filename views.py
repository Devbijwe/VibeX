import email
import io
import os
import urllib.parse
import uuid
import base64
import json
from datetime import datetime
from werkzeug.utils import secure_filename
from unicodedata import name
from warnings import catch_warnings
from flask import Flask, Response, redirect, render_template, request, session, jsonify, url_for
from jinja2 import Template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

# from flask_ngrok import run_with_ngrok
from __init__ import app, db, cache
from models import *

# ✅ Load configuration
with open('config.json', "r") as c:
    params = json.load(c)['params']

# ✅ Very long cache timeout (10 years)
CACHE_TIMEOUT = 315360000  

# =================== Routes ===================

@app.route("/", methods=["GET", "POST", "PUT", "DELETE", "HEAD"])
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix="index")
def index():
    song_id = Songs.get_random_song_id()
    return redirect(url_for('playsong', song_id=song_id))


@app.route("/play")
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=lambda: f"play_{request.args.get('song_id')}_{request.args.get('action')}")
def playsong():
    song_id = request.args.get('song_id')
    action = request.args.get('action')
    current_song = Songs.query.get(song_id)
    pageTitle = "Home"

    if action and current_song:
        if action == "prev":
            previous_song_id = current_song.get_previous_song_id()
            return redirect(url_for('playsong', song_id=previous_song_id))
        if action == "next":
            next_song_id = current_song.get_next_song_id()
            return redirect(url_for('playsong', song_id=next_song_id))

    if current_song is None:
        song_id = Songs.get_random_song_id()

    if song_id:
        song = Songs.query.get(song_id)
        pageTitle = song.songName

    return render_template("player.html", song_id=song_id, pageTitle=pageTitle)


@app.route("/mob", methods=["GET", "POST", "PUT", "DELETE", "HEAD"])
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix="mob_index")
def indexmob():
    return render_template("indexmob.html", params=params)


@app.route("/xyz-account", methods=["GET", "POST"])
def account():
    if request.method == 'POST':
        artist = request.form.get("artist")
        songName = request.form.get("songname")
        album = request.form.get("album")
        userid = request.form.get("userid")
        date = datetime.now()

        # Process and store uploaded files as BLOBs
        filesongaudio = request.files.get("filesongaudio").read()
        filesonglyrics = request.files.get("filesonglyrics").read()
        filesongbg = request.files.get("filesongbg").read()
        songId = uuid.uuid4().hex[:10]

        songEntry = Songs(
            songId=songId,
            songName=songName,
            songArtist=artist,
            songAlbum=album,
            uploadId=userid,
            date=date,
            songLyrics=filesonglyrics,
            songBg=filesongbg,
            songAudio=filesongaudio
        )

        db.session.add(songEntry)
        db.session.commit()

        # ✅ Invalidate ALL caches after upload
        cache.delete("all_songs")
        cache.delete(f"song_{songId}")
        cache.delete(f"lyrics_{songId}")
        cache.delete(f"bg_{songId}")
        cache.delete(f"audio_{songId}")
        cache.delete(f"play_{songId}_None")
        cache.delete("index")
        cache.delete("mob_index")

    return render_template("account.html")


# =================== API Endpoints ===================

@app.route("/get-songs", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix="all_songs")
def get_songs():
    songs = Songs.query.all()
    song_list = []

    for song in songs:
        song_lyrics_base64 = base64.b64encode(song.songLyrics).decode('utf-8')
        song_bg_base64 = base64.b64encode(song.songBg).decode('utf-8')
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
        }
        song_list.append(song_data)

    return jsonify(songs=song_list)


@app.route("/get-song/<string:song_id>", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=lambda: f"song_{request.view_args['song_id']}")
def get_song_by_id(song_id):
    song = Songs.query.get(song_id)
    if not song:
        return jsonify(error="Song not found"), 404

    song_data = {
        "songId": song.songId,
        "songName": song.songName,
        "songArtist": song.songArtist,
        "songAlbum": song.songAlbum,
        "uploadId": song.uploadId,
        "date": song.date.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return jsonify(song=song_data)


# =================== Download Endpoints ===================

@app.route("/download/song-lyrics/<string:song_id>", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=lambda: f"lyrics_{request.view_args['song_id']}")
def download_song_lyrics(song_id):
    song = Songs.query.get(song_id)
    if not song:
        return jsonify(error="Song not found"), 404
    return Response(io.BytesIO(song.songLyrics), content_type="text/plain")


@app.route("/download/song-bg/<string:song_id>", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=lambda: f"bg_{request.view_args['song_id']}")
def download_song_bg(song_id):
    song = Songs.query.get(song_id)
    if not song:
        return jsonify(error="Song not found"), 404
    return Response(io.BytesIO(song.songBg), content_type="video/mp4")


@app.route("/download/song-audio/<string:song_id>", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix=lambda: f"audio_{request.view_args['song_id']}")
def download_song_audio(song_id):
    song = Songs.query.get(song_id)
    if not song:
        return jsonify(error="Song not found"), 404
    return Response(io.BytesIO(song.songAudio), content_type="audio/mpeg")


@app.route("/loader")
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix="loader_page")
def loader():
    return render_template("loader.html")


# =================== Context Processor ===================

@app.context_processor
@cache.cached(timeout=CACHE_TIMEOUT, key_prefix="context_processor")
def default():
    user = 0
    favsong = []
    cred = Songs.query.all()
    return dict(cred=cred, fav=favsong)
