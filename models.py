from datetime import datetime
from __init__ import app,db
from sqlalchemy.dialects.postgresql import BYTEA



class Users(db.Model):
    __tablename__ = 'users'
    userId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    bio = db.Column(db.String(100), nullable=True)
    favSongs = db.Column(db.String(1000), nullable=True)
    date = db.Column(db.String(12), nullable=True)

# class Songs(db.Model):
#     __tablename__ = 'songs'
#     songId = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     songName = db.Column(db.String(75), nullable=False)
#     songArtist = db.Column(db.String(50), nullable=False)
#     songLyrics = db.Column(db.String(75), nullable=False)
#     songBg = db.Column(db.String(75), nullable=True)
#     songAlbum = db.Column(db.String(50), nullable=False)
#     uploadId = db.Column(db.String(20), nullable=True)
#     date = db.Column(db.String(12), nullable=True)

class Songs(db.Model):
    songId = db.Column(db.Integer, primary_key=True)
    songName = db.Column(db.String(75), nullable=False)
    songArtist = db.Column(db.String(50), nullable=False)
    songLyrics = db.Column( BYTEA, nullable=True)  # Store lyrics as BLOB
    songBg = db.Column( BYTEA, nullable=True)  # Store background as BLOB
    songAlbum = db.Column(db.String(50), nullable=False)
    uploadId = db.Column(db.String(20), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())
    songAudio = db.Column( BYTEA, nullable=True)  # Store audio as BLOB



class Favsongs(db.Model):
    __tablename__ = 'favsongs'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, nullable=False)
    songId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12), nullable=True)

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.String(14), nullable=False)
    email = db.Column(db.String(25), nullable=False)
    feedback = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(12), nullable=True)
