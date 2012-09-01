from skills import db

class User(db.Document):
	username = db.StringField(max_length=50, required=True, unique=True)
	password = db.StringField(max_length=50, required=True)
	firstname = db.StringField(max_length=50, required=True)
	lastname = db.StringField(max_length=50, required=True)
	isadmin = db.BooleanField(default=False)
	skills = db.ListField(db.EmbeddedDocumentField('Skill'))

class Skill(db.EmbeddedDocument):
	name = db.StringField(max_length=50, required=True, primary_key=True)
	category = db.StringField(max_length=50, required=True)
	score = db.IntField(required=True)
	wanttolearn = db.BooleanField(default=False)

class Category(db.Document):
	name = db.StringField(max_length=50, required=True)
	skills = db.ListField(db.StringField(max_length=50))
	
	meta = {
		'indexes': ['name']
	}

class ScoreDescription(db.Document):
	score = db.IntField(required=True)
	description = db.StringField(max_length=50, required=True)