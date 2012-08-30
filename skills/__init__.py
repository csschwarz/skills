from __future__ import with_statement
from contextlib import closing
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/skills.db'
DEBUG = True
SECRET_KEY = 'dev key'

app = Flask(__name__)
app.config.from_object(__name__)
db = SQLAlchemy(app)

@app.teardown_request
def teardown_request(exception=None):
	db.session.remove()

import skills.login
import skills.forms
import skills.admin