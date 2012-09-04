from skills import app
from skills.models import User
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from wtforms import Form, TextField, RadioField, validators, PasswordField
from create_user import create_user
from login_user import login_user

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
		return login_user(form)
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
