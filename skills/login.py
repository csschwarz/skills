from skills import app
from skills.models import User
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from wtforms import Form, TextField, RadioField, validators, PasswordField

class LoginForm(Form):
	username = TextField('username', [validators.Required()])
	password = PasswordField('password', [validators.Required()])

class RegistrationForm(LoginForm):
	firstname = TextField('firstname', [validators.Required()])
	lastname = TextField('lastname', [validators.Required()])

@app.route('/', methods=['GET'])
def index():
	form = LoginForm(request.form)
	if session.get('username') and session.get('isadmin'):
		return redirect(url_for('admin'))
	elif session.get('username'):
		return redirect(url_for('form', pagenum=0))
	return render_template('index.html', form=form)

@app.route('/', methods=['POST'])
def index_post():
	form = LoginForm(request.form)
	if form.validate():
		user = User.objects(username=request.form['username'], password=request.form['password'])
		if len(user) == 1:
			user = user.get()
			session['username'] = request.form['username']
			session.pop('isadmin', None)
			flash('Login successful!')
			return redirect(create_url(user))
		else:
			error = 'Invalid username or password'
	else:
		error = "Can't leave any fields blank"
	return render_template('index.html', form=form, error=error)

def create_url(user):
	if user.isadmin:
		session['isadmin'] = True
		return url_for('admin')
	else:
		return url_for('form', pagenum=0)

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
		if User.objects(username=request.form['username']).count():
			error = "Username already taken"
		else:
			newuser = User()
			form.populate_obj(newuser)
			newuser.save()
			flash('Registration successful!')
			return redirect(url_for('index'))
	elif request.method == 'POST':
		error = "Can't leave any fields blank"
	return render_template('register.html', form=form, error=error)
