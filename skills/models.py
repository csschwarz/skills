from skills import db

class UserSkill(db.Model):
	userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	skill = db.Column(db.String, db.ForeignKey('skill.name'), primary_key=True)
	score = db.Column(db.Integer, nullable=False)
	def __init__(self, userid, skill, score):
		self.userid = userid
		self.skill = skill
		self.score = score

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, unique=True)
	password = db.Column(db.String, nullable=False)
	firstname = db.Column(db.String, nullable=False)
	lastname = db.Column(db.String, nullable=False)
	isadmin = db.Column(db.Integer, nullable=False, default=0)
	def __init__(self, username, password, firstname, lastname, isadmin=0):
		self.username = username
		self.password = password
		self.firstname = firstname
		self.lastname = lastname
		self.isadmin = isadmin

class Skill(db.Model):
	name = db.Column(db.String, primary_key=True)
	category = db.Column(db.String, nullable=False)
	def __init__(self, name, category):
		self.name = name
		self.category = category

class ScoreDescription(db.Model):
	score = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String, nullable=False)
	def __init__(self, score, description):
		self.score = score
		self.description = description

