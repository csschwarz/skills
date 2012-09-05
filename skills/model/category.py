from skills import db

class Category(db.Document):
	name = db.StringField(max_length=50, required=True)
	skills = db.ListField(db.StringField(max_length=50))
	
	meta = {
		'indexes': ['name']
	}

class ScoreDescription(db.Document):
	score = db.IntField(required=True)
	description = db.StringField(max_length=50, required=True)