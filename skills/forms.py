from skills import app, query_db
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from wtforms import Form, TextField, RadioField, validators, PasswordField

@app.route('/form/<int:pagenum>', methods=['GET', 'POST'])
def form(pagenum):
	if not session.get('username'):
		flash('You need to login first!')
		return redirect(url_for('index'))
	error = None
	categories = [item['category'] for item in query_db('select category from skilltab group by category order by category')]
	if not 0 <= pagenum < len(categories):
		flash('Not a valid page.')
		return redirect(url_for('index'))
	scoredesc = {elem['score']: elem['description'] for elem in query_db('select * from scoredescription order by score')}
	userid = query_db('select * from user where username=?', [session.get('username')], one=True)['id']
	# Empty class to create form
	class F(Form):
		pass
	# Empty class to repopulate form from saved data
	class Saved:
		pass

	skillslist = query_db('select name from skilltab where category=? order by name', [categories[pagenum]])
	for item in skillslist:
		setattr(F, item['name'], RadioField(item['name'], [validators.Required()], 
				choices=[('1',''),('2',''),('3',''),('4',''),('5','')]))
	saved_skills = query_db('select skill, score from userskill where userid=?', [userid])
	for item in saved_skills:
		setattr(Saved, item['skill'], item['score'])
	form = F(request.form, obj=Saved())
	if request.method == 'POST' and form.validate():
		for field in request.form:
			g.db.execute('replace into userskill(userid, skill, score) values (?, ?, ?)',
					[userid, field, request.form[field]])
			g.db.commit()
		flash('Saved successfully!')
		return redirect(url_for('form', pagenum=pagenum))
	elif request.method == 'POST':
		error = "You didn't fill out the whole form. Please do that."
	return render_template('form.html', form=form, categories=categories, pagenum=pagenum, scoredesc=scoredesc, error=error)
