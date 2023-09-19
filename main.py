
import email
import os
import urllib.parse
from werkzeug.utils import secure_filename
from unicodedata import name
from warnings import catch_warnings
from flask import Flask, redirect,render_template, request,session
from jinja2 import Template

import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_mail import Mail
from sqlalchemy.exc import IntegrityError 
# from flask_ngrok import run_with_ngrok
with open('config.json',"r") as c:
    params=json.load(c)['params']
local_server=True
app = Flask(__name__,template_folder="templates")
#run_with_ngrok(app)
app.config.update(
MAIL_SERVER ='smtp.gmail.com' ,
MAIL_PORT ='465',
MAIL_USE_SSL=True,
MAIL_USERNAME=params['gmail_user'],
MAIL_PASSWORD=params['gmail_pswd'])
mail=Mail(app)
app.secret_key = 'super-secret-key'


if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_url']
    # app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@localhost/musics"
else:
    app.config['SQLALCHEMY_DATABASE_URI'] =  params['prod_url']
db= SQLAlchemy(app)

class Users(db.Model):
    userId=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50),nullable=False)    
    mobile=db.Column(db.String(15),nullable=False)
    email=db.Column(db.String(50),nullable=False)
    password=db.Column(db.String(30),nullable=False)
    bio=db.Column(db.String(100),nullable=True)
    favSongs=db.Column(db.String(1000),nullable=True)
    date=db.Column(db.String(12),nullable=True)
class Songs(db.Model):
    songId = db.Column(db.Integer, primary_key=True)
    songName = db.Column(db.String(75), nullable=False)
    songArtist = db.Column(db.String(50),nullable=False )
    songLyrics = db.Column(db.String(75),nullable=False)
    songBg = db.Column(db.String(75),nullable=True)
    songAlbum = db.Column(db.String(50),nullable=False)
    uploadId = db.Column(db.String(20),nullable=True)
    date = db.Column(db.String(12),nullable=True)
class Favsongs(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    userId=db.Column(db.Integer,nullable=False)
    songId = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(12),nullable=True)
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    mobile = db.Column(db.String(14),nullable=False )
    email = db.Column(db.String(25),nullable=False)
    feedback = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(12),nullable=True)
with app.app_context():
    db.create_all()
@app.route("/",methods=["GET","POST","PUT","DELETE","HEAD"])
def index():
    # return render_template("indexmob.html",params=params)
    return render_template("index.html",params=params)
@app.route("/mob",methods=["GET","POST","PUT","DELETE","HEAD"])
def indexmob():
    return render_template("indexmob.html",params=params)

@app.route("/fav/adder/<string:songId>",methods=["GET","POST","PUT","DELETE","HEAD"])
def favAdder(songId):
    user=0
    fav=Favsongs.query.filter_by(userId=user,songId=songId).first()
    if fav==None:
        favEntry=Favsongs(userId=user,songId=songId,date=datetime.now())
        db.session.add(favEntry)
        db.session.commit()
        
    return redirect("/")

@app.route("/acc" ,methods=["GET","POST","PUT","DELETE","HEAD"])
def account():
    if (request.method=='POST'):
        # songname=request.form.get("songname") 
        # songlyrics=request.form.get("songlyrics")
        artist=request.form.get("artist")
        album=request.form.get("album")  
        userid=request.form.get("userid")  
        date=request.form.get("date")
        app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['uploadSong'])
        f=request.files["filesongname"]
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
        app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['uploadLyrics'])
        #app.config['UPLOAD_FOLDER']=params['uploadLyrics']
        g=request.files["filesonglyrics"]
        g.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(g.filename)))
        app.config['UPLOAD_FOLDER']= os.path.abspath("../"+params['uploadBg'])
        h=request.files["filesongbg"]
        h.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(h.filename)))
        songEntry=Songs(songName=secure_filename(f.filename),songBg=secure_filename(h.filename),songLyrics=secure_filename(g.filename),songAlbum=album ,songArtist=artist,uploadId=userid,date=datetime.now())
        db.session.add(songEntry)
        db.session.commit()   
    return redirect("/")
@app.route("/loader")
def loader():
    return render_template("loader.html")

@app.context_processor
def default():
    user=0
    favsong=[]
    fav=Favsongs.query.filter_by(userId=user).all()
    for item in fav:
        favsong+=Songs.query.filter_by(songId=item.songId).all()
    cred=Songs.query.all()
    #cred=cred[2].songName
    return dict(cred=cred,fav=favsong)
if __name__=="__main__":
    #app.run()
    app.run(debug=True,host="0.0.0.0",port=2000)