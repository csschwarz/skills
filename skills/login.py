from skills.model import User
from flask import current_app, Blueprint, Flask, request, session, redirect, url_for, abort, render_template, flash
from wtforms import Form, TextField, RadioField, validators, PasswordField
from login_user import login_user

user = Blueprint('user', __name__)

class LoginForm(Form):
	username = TextField('username', [validators.Required()])
	password = PasswordField('password', [validators.Required()])

class RegistrationForm(LoginForm):
	firstname = TextField('firstname', [validators.Required()])
	lastname = TextField('lastname', [validators.Required()])

@user.route('/', methods=['GET'])
def index():
	form = LoginForm(request.form)
	if session.get('username') and session.get('isadmin'):
		return redirect(url_for('admin_page.admin'))
	if session.get('username'):
		return redirect(url_for('form', pagenum=0))
	return render_template('index.html', form=form)

@user.route('/', methods=['POST'])
def index_post():
	form = LoginForm(request.form)
	if form.validate():
		return login_user(form)
	return render_template('index.html', form=form, error="Can't leave any fields blank")

@user.route('/logout/')
def logout():
	session.pop('username', None)
	session.pop('isadmin', None)
	flash('You have been logged out.')
	return redirect(url_for('user.index'))

@user.route('/register/', methods=['GET'])
def register():
	return render_template('register.html', form=RegistrationForm(request.form), error=None)

@user.route('/register/', methods=['POST'])
def register_post():
	error = "Can't leave any fields blank"
	form = RegistrationForm(request.form)
	if form.validate():
		new_user = User()
		form.populate_obj(new_user)
		if new_user.create():
			flash('Registration successful!')
			return redirect(url_for('user.index'))
		else:
			error = "User already exists"
	return render_template('register.html', form=form, error=error)	
