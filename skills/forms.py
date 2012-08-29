from skills import app, db
from skills.models import User, Skill, UserSkill, ScoreDescription
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from wtforms import Form, RadioField, validators

@app.route('/form/<int:pagenum>', methods=['GET', 'POST'])
def form(pagenum):
	if not session.get('username'):
		flash('You need to login first!')
		return redirect(url_for('index'))
	error = None
	categories = [item.category for item in Skill.query.group_by(Skill.category).order_by(Skill.category).all()]
	if not 0 <= pagenum < len(categories):
		flash('Not a valid page.')
		return redirect(url_for('index'))
	scoredesc = {elem.score: elem.description for elem in ScoreDescription.query.order_by(ScoreDescription.score).all()}
	user = User.query.filter_by(username=session.get('username')).first()
	# Empty class to create form
	class F(Form):
		pass
	# Empty class to repopulate form from saved data
	class Saved:
		pass

	skillslist = Skill.query.filter_by(category=categories[pagenum]).order_by(Skill.name).all()
	for item in skillslist:
		setattr(F, item.name, RadioField(item.name, [validators.Required()], 
				choices=[('1',''),('2',''),('3',''),('4',''),('5','')]))
	saved_skills = UserSkill.query.filter_by(userid=user.id).all()
	for item in saved_skills:
		setattr(Saved, item.skill, item.score)
	form = F(request.form, obj=Saved())
	if request.method == 'POST' and form.validate():
		for field in request.form:
			db.session.merge(UserSkill(user.id, field, request.form[field]))
		db.session.commit()
		flash('Saved successfully!')
		return redirect(url_for('form', pagenum=pagenum))
	elif request.method == 'POST':
		error = "You didn't fill out the whole form. Please do that."
	return render_template('form.html', form=form, categories=categories, pagenum=pagenum, scoredesc=scoredesc, error=error)
