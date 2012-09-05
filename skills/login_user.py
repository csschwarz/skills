from skills.model import User
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from wtforms import Form

def login_user(form):
	user = User.objects(username=request.form['username'], password=request.form['password'])
	if len(user) == 1:
		user = user.get()
		session['username'] = request.form['username']
		session.pop('isadmin', None)
		flash('Login successful!')
		return redirect(_role_specific_url(user))
	return render_template('index.html', form=form, error='Invalid username or password')

def _role_specific_url(user):
	if user.isadmin:
		session['isadmin'] = True
		return url_for('admin')
	return url_for('form', pagenum=0)
