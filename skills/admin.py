from skills import app, query_db
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from wtforms import Form, TextField, RadioField, validators, PasswordField

@app.route('/admin/')
def admin():
	if not session.get('isadmin'):
		abort(401)
	users = query_db('select id, username, firstname, lastname from user where id in \
			(select distinct userid from userskill) order by lastname')
	allskills = query_db('select name, category from skilltab order by category, name')
	return render_template('admin_index.html', users=users, allskills=allskills)

@app.route('/admin/viewuser/<int:userid>')
def admin_userstats(userid):
	if not session.get('isadmin'):
		abort(401)
	scoredesc = {elem['score']: elem['description'] for elem in query_db('select * from scoredescription order by score')}
	user = query_db('select * from user where id=?', [userid], one=True)
	categories = [item['category'] for item in query_db('select category from skilltab group by category order by category')]
	skills = dict()
	for category in categories:
		skills[category] = query_db('select u.skill, u.score from userskill as u \
				join skilltab as s on u.skill=s.name where u.userid=? and s.category=? order by u.score desc', [userid, category])
	return render_template('admin_userstats.html', user=user, skills=skills, categories=categories, scoredesc=scoredesc)

@app.route('/admin/viewskill/<skill>')
def admin_skillstats(skill):
	if not session.get('isadmin'):
		abort(401)
	scoredesc = {elem['score']: elem['description'] for elem in query_db('select * from scoredescription order by score')}
	users = query_db('select u.id, u.firstname, u.lastname, us.score from user as u \
			join userskill as us on u.id=us.userid \
			where us.skill=? order by us.score desc', [skill])
	return render_template('admin_skillstats.html', skillname=skill, users=users, scoredesc=scoredesc)
