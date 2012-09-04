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
	if session.get('username'):
		return redirect(url_for('form', pagenum=0))
	return render_template('index.html', form=form)

@app.route('/', methods=['POST'])
def index_post():
	form = LoginForm(request.form)
	if form.validate():
		return login(form)
	return render_template('index.html', form=form, error="Can't leave any fields blank")

@app.route('/logout/')
def logout():
	session.pop('username', None)
	session.pop('isadmin', None)
	flash('You have been logged out.')
	return redirect(url_for('index'))

@app.route('/register/', methods=['GET'])
def register():
	return render_template('register.html', form=RegistrationForm(request.form), error=None)

@app.route('/register/', methods=['POST'])
def register_post():
	form = RegistrationForm(request.form)
	if form.validate():
		return create_user(form)
	return render_template('register.html', form=form, error="Can't leave any fields blank")

def create_user(form):
	if user_exists():
		return render_template('register.html', form=form, error="Username already taken")
	new_user = User()
	form.populate_obj(new_user)
	new_user.save()
	flash('Registration successful!')
	return redirect(url_for('index'))

def user_exists():
	return User.objects(username=request.form['username']).count()	

def login(form):
	user = User.objects(username=request.form['username'], password=request.form['password'])
	if len(user) == 1:
		user = user.get()
		session['username'] = request.form['username']
		session.pop('isadmin', None)
		flash('Login successful!')
		return redirect(role_specific_url(user))
	return render_template('index.html', form=form, error='Invalid username or password')

def role_specific_url(user):
	if user.isadmin:
		session['isadmin'] = True
		return url_for('admin')
	return url_for('form', pagenum=0)
