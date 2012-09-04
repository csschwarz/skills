from skills.models import User
from flask import Flask, request, redirect, url_for, render_template, flash
from wtforms import Form

def create_user(form):
	if _user_exists():
		return render_template('register.html', form=form, error="Username already taken")
	new_user = User()
	form.populate_obj(new_user)
	new_user.save()
	flash('Registration successful!')
	return redirect(url_for('index'))

def _user_exists():
	return User.objects(username=request.form['username']).count()
