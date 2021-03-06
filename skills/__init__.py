from flask import Flask
from mongoengine import *
from flask.ext.mongoengine import MongoEngine

db = MongoEngine()

def create_app(config_filename):
	app = Flask(__name__) 
	app.config.from_pyfile(config_filename) 

	from skills.login import user
	from skills.admin import admin_page
	from skills.forms import form_page
	
	app.register_blueprint(user) 
	app.register_blueprint(admin_page) 
	app.register_blueprint(form_page)
	
	connect(app.config['MONGODB_DB'])

	return app