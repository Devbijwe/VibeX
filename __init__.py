
import email
import os
import urllib.parse
from werkzeug.utils import secure_filename
from unicodedata import name
from warnings import catch_warnings
from flask import Flask, redirect,render_template, request,session
from jinja2 import Template
from flask_cors import CORS
import json
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_mail import Mail
from sqlalchemy.exc import IntegrityError 
with open('config.json',"r") as c:
    params=json.load(c)['params']

local_server=True
app = Flask(__name__,template_folder="templates")
CORS(app)
#run_with_ngrok(app)
app.config.update(
MAIL_SERVER ='smtp.gmail.com' ,
MAIL_PORT ='465',
MAIL_USE_SSL=True,
MAIL_USERNAME=params['gmail_user'],
MAIL_PASSWORD=params['gmail_pswd'])
mail=Mail(app)
app.secret_key = 'super-secret-key'


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or "postgresql://22devendrabijwe:PToEG2huQ1iv@ep-round-hill-10279815.ap-southeast-1.aws.neon.tech/vibex"
 
    
db= SQLAlchemy(app)

from views import *

with app.app_context():
    db.create_all()

# if __name__=="__main__":
#     #app.run()
#     app.run(debug=True,host="0.0.0.0",port=2000)

