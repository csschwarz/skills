from skills import app, db
from skills.models import User, Skill, UserSkill, ScoreDescription
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash

@app.route('/admin/')
def admin():
	if not session.get('isadmin'):
		abort(401)
	users = User.query.filter(User.id.in_(db.session.query(UserSkill.userid).distinct(UserSkill.userid))).all()
	allskills = db.session.query(Skill.name, Skill.category).order_by(Skill.category, Skill.name).all()
	return render_template('admin_index.html', users=users, allskills=allskills)

@app.route('/admin/viewuser/<int:userid>')
def admin_userstats(userid):
	if not session.get('isadmin'):
		abort(401)
	scoredesc = {elem.score: elem.description for elem in ScoreDescription.query.order_by(ScoreDescription.score).all()}
	user = User.query.get(userid)
	categories = [item.category for item in Skill.query.group_by(Skill.category).order_by(Skill.category).all()]
	skills = dict()
	for category in categories:
		skills[category] = db.session.query(UserSkill.skill, UserSkill.score).\
											 join(Skill).filter(UserSkill.userid == userid, Skill.category == category).\
											 order_by(UserSkill.score.desc()).all()
	return render_template('admin_userstats.html', user=user, skills=skills, categories=categories, scoredesc=scoredesc)

@app.route('/admin/viewskill/<skill>')
def admin_skillstats(skill):
	if not session.get('isadmin'):
		abort(401)
	scoredesc = {elem.score: elem.description for elem in ScoreDescription.query.order_by(ScoreDescription.score).all()}
	users = db.session.query(User.firstname, User.lastname, UserSkill.score).\
			join(UserSkill).filter_by(skill=skill).order_by(UserSkill.score.desc()).all()
	return render_template('admin_skillstats.html', skillname=skill, users=users, scoredesc=scoredesc)
