from flask import Flask
from flask.ext.mongoengine import MongoEngine

MONGODB_DB = 'hacksaw'
SECRET_KEY = 'dev key'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
db = MongoEngine(app)

import skills.login
import skills.forms
import skills.admin