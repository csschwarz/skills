from skills import app, db
from skills.models import User
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from wtforms import Form, TextField, RadioField, validators, PasswordField

class LoginForm(Form):
	username = TextField('username', [validators.Required()])
	password = PasswordField('password', [validators.Required()])

class RegistrationForm(LoginForm):
	firstname = TextField('firstname', [validators.Required()])
	lastname = TextField('lastname', [validators.Required()])

@app.route('/', methods=['GET', 'POST'])
def index():
	form = LoginForm(request.form)
	error = None
	if session.get('username') and session.get('isadmin'):
		return redirect(url_for('admin'))
	elif session.get('username'):
		return redirect(url_for('form', pagenum=0))
	if request.method == 'POST' and form.validate():
		user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
		if not user is None:
			session['username'] = request.form['username']
			session.pop('isadmin', None)
			flash('Login successful!')
			if user.isadmin:
				session['isadmin'] = True
				return redirect(url_for('admin'))
			else:
				return redirect(url_for('form', pagenum=0))
		else:
			error = 'Invalid username or password'
	elif request.method == 'POST':
		error = "Can't leave any fields blank"
	return render_template('index.html', form=form, error=error)

@app.route('/logout/')
def logout():
	session.pop('username', None)
	session.pop('isadmin', None)
	flash('You have been logged out.')
	return redirect(url_for('index'))

@app.route('/register/', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	error = None
	if request.method == 'POST' and form.validate():
		if User.query.filter_by(username=request.form['username']).count():
			error = "Username already taken"
		else:
			newuser = User(request.form['username'], request.form['password'], 
					request.form['firstname'], request.form['lastname'])
			db.session.add(newuser)
			db.session.commit()
			flash('Registration successful!')
			return redirect(url_for('index'))
	elif request.method == 'POST':
		error = "Can't leave any fields blank"
	return render_template('register.html', form=form, error=error)
