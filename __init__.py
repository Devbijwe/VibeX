
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
from flask_caching import Cache  # ✅ Added for in-memory caching

with open('config.json',"r") as c:
    params=json.load(c)['params']

local_server=True
app = Flask(__name__,template_folder="templates")
CORS(app)

app.secret_key = 'super-secret-key'


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") or "postgresql://bytestardb:ByteStarDB@103.194.228.122:5432/vibex-backend" or "postgresql://22devendrabijwe:PToEG2huQ1iv@ep-round-hill-10279815.ap-southeast-1.aws.neon.tech/vibex"
 
    
db= SQLAlchemy(app)

# ✅ Configure in-memory cache
cache_config = {
    "CACHE_TYPE": "SimpleCache",         # In-memory cache
    "CACHE_DEFAULT_TIMEOUT": 315360000   # 10 years in seconds
}

app.config.from_mapping(cache_config)
cache = Cache(app)

from views import *

with app.app_context():
    db.create_all()



