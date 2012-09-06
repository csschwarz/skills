from skills.model import *
from flask import current_app, Blueprint, Flask, request, session, redirect, url_for, abort, render_template, flash
from wtforms import Form, RadioField

form_page = Blueprint('form_page', __name__)

@form_page.route('/form/<int:pagenum>', methods=['GET', 'POST'])
def form(pagenum):
	if not session.get('username'):
		flash('You need to login first!')
		return redirect(url_for('index'))
	error = None
	categories = [item.name for item in Category.objects.only('name')]
	if not 0 <= pagenum < len(categories):
		flash('Not a valid page.')
		return redirect(url_for('index'))
	scoredesc = {item.score: item.description for item in ScoreDescription.objects}
	user = User.objects(username=session.get('username')).get()
	# Empty class to create form
	class F(Form):
		pass
	# Empty class to repopulate form from saved data
	class Saved:
		pass

	category = Category.objects(name=categories[pagenum]).get()
	skillslist = category.skills
	skillslist.sort()
	for skill in skillslist:
		setattr(F, skill, RadioField(skill, choices=[('1',''),('2',''),('3',''),('4',''),('5','')]))
	for item in user.skills:
		setattr(Saved, item.name, item.score)
	form = F(request.form, obj=Saved())
	if request.method == 'POST':
		for field in request.form:
			curobj = User.objects(pk=user.pk, skills__name=field)
			if curobj:
				curobj.update(set__skills__S__score=request.form[field])
			else:
				user.skills.append(Skill(name=field, category=category.name, score=request.form[field]))
				user.save()
		flash('Saved successfully!')
		return redirect(url_for('form_page.form', pagenum=pagenum))
	return render_template('form.html', form=form, categories=categories, 
			pagenum=pagenum, scoredesc=scoredesc, error=error, title='Capabilities')
