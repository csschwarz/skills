from skills.models import *

User.drop_collection()
Category.drop_collection()
ScoreDescription.drop_collection()

User(username='test', password='t', firstname='Test', lastname='User').save()
User(username='test2', password='t', firstname='Test', lastname='User 2').save()
User(username='admin', password='admin', firstname='Admin', lastname='Adminson', isadmin=True).save()

ScoreDescription(score=1, description="1 Desc").save()
ScoreDescription(score=2, description="2 Desc").save()
ScoreDescription(score=3, description="3 Desc").save()
ScoreDescription(score=4, description="4 Desc").save()
ScoreDescription(score=5, description="5 Desc").save()

testing_skills = [
	'Cucumber',
	'Selenium',
	'Manual Testing'
]
programming_skills = [
	'Java',
	'Groovy',
	'Python'
]

Category(name='Testing', skills=testing_skills).save()
Category(name='Programming', skills=programming_skills).save()
