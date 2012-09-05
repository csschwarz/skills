from skills.model import *
from flask import current_app, Blueprint, Flask, request, session, redirect, url_for, abort, render_template, flash 

admin_page = Blueprint('admin_page', __name__)

@admin_page.route('/admin/')
def admin():
	if not session.get('isadmin'):
		abort(401)
	users = User.objects(skills__not__size=0).order_by('lastname')
	allskills = Category.objects
	return render_template('admin_index.html', users=users, allskills=allskills)

@admin_page.route('/admin/viewuser/<username>')
def admin_userstats(username):
	if not session.get('isadmin'):
		abort(401)
	scoredesc = {item.score: item.description for item in ScoreDescription.objects}
	user = User.objects(username=username).get()
	categories = [item.name for item in Category.objects.only('name')]
	skills = sorted(user.skills, key=lambda skill: skill['score'], reverse=True)
	skills = sorted(skills, key=lambda skill: skill['category'])
	return render_template('admin_userstats.html', user=user, skills=skills, categories=categories, scoredesc=scoredesc)

@admin_page.route('/admin/viewskill/<skill>')
def admin_skillstats(skill):
	if not session.get('isadmin'):
		abort(401)
	scoredesc = {item.score: item.description for item in ScoreDescription.objects}
	users = User.objects(skills__name=skill)
	userscores = []
	for user in users:
		userscores.append({'user': user, 'score': [ x.score for x in user.skills if x.name==skill ][0]})
	userscores = sorted(userscores, key=lambda userscore: userscore['score'], reverse=True)
	return render_template('admin_skillstats.html', skillname=skill, userscores=userscores, scoredesc=scoredesc)
