from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, g

### BEGIN CONFIG ###

DATABASE = '/tmp/skills.db'
DEBUG = True
SECRET_KEY = 'dev key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# Use this from the shell to setup database
def init_db(test=False):
	with closing(connect_db()) as db:
		with app.open_resource('test_schema.sql' if test else 'schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

# Query the database. Returns dict.
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	if(hasattr(g, 'db')):
		g.db.close()

### END CONFIG ###

import skills.login
import skills.forms
import skills.admin