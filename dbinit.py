from skills import db
from skills.models import *

db.drop_all()
db.create_all()

test = User('test', 't', 'Test', 'User')
admin = User('admin', 'admin', 'Admin', 'Adminson', 1)
db.session.add(test)
db.session.add(admin)

skill = Skill('Java', 'Programming')
skill2 = Skill('Groovy', 'Programming')
db.session.add(skill)
db.session.add(skill2)

sd1 = ScoreDescription(1, 'Don\'t know it')
sd2 = ScoreDescription(2, 'Want to learn it')
sd3 = ScoreDescription(3, 'Know it')
sd4 = ScoreDescription(4, 'Can do it alone')
sd5 = ScoreDescription(5, 'Can teach it')
db.session.add(sd1)
db.session.add(sd2)
db.session.add(sd3)
db.session.add(sd4)
db.session.add(sd5)

db.session.execute('insert into user_skill(userid, skill, score) values (1, "Java", 3)')

db.session.commit()