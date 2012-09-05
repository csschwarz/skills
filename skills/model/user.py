from skills import db

class User(db.Document):
	username = db.StringField(max_length=50, required=True, unique=True)
	password = db.StringField(max_length=50, required=True)
	firstname = db.StringField(max_length=50, required=True)
	lastname = db.StringField(max_length=50, required=True)
	isadmin = db.BooleanField(default=False)
	skills = db.ListField(db.EmbeddedDocumentField('Skill'))

	def create(self):
		if self._exists():
			return False
		self.save()
		return True

	def _exists(self):
		return User.objects(username=self.username).count()


class Skill(db.EmbeddedDocument):
	name = db.StringField(max_length=50, required=True, primary_key=True)
	category = db.StringField(max_length=50, required=True)
	score = db.IntField(required=True)
	wanttolearn = db.BooleanField(default=False)