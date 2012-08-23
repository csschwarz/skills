from __future__ import with_statement
from contextlib import closing
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from wtforms import Form, TextField, RadioField, validators, PasswordField

### BEGIN CONFIG ###

DATABASE = '/tmp/skills.db'
DEBUG = True
SECRET_KEY = 'dev key'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

# Use this from the shell to setup database
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()

# Query the database. Returns dict.
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	if(hasattr(g, 'db')):
		g.db.close()

### END CONFIG ###
### BEGIN LOGIN & REGISTRATION ###

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
	if request.method == 'POST' and form.validate():
		user = query_db('select count(*) as count from user where username=?', [request.form['username']], one=True)
		if user['count'] == 1:
			session['logged_in'] = True
			session['username'] = request.form['username']
			flash('Login successful!')
			return redirect(url_for('form'))
		else:
			error = 'Invalid username or password'
	elif request.method == 'POST':
		error = "Can't leave any fields blank"
	return render_template('index.html', form=form, error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	error = None
	if request.method == 'POST' and form.validate():
		if query_db('select count(*) as count from user where username=?', [request.form['username']], one=True)['count']:
			error = "Username already taken"
		else:
			g.db.execute('insert into user(username, password, firstname, lastname) values(?, ?, ?, ?)',
					[request.form['username'], request.form['password'], request.form['firstname'], request.form['lastname']])
			g.db.commit()
			flash('Registration successful!')
			return redirect(url_for('index'))
	elif request.method == 'POST':
		error = "Can't leave any fields blank"
	return render_template('register.html', form=form, error=error)

### END LOGIN & REGISTRATION ###
### BEGIN MAIN FORM ###

@app.route('/form', methods=['GET', 'POST'])
def form():
	class F(Form):
		pass

	error = None
	skillslist = query_db('select name from skilltab')
	for item in skillslist:
		setattr(F, item['name'], RadioField(item['name'], [validators.Required()], 
				choices=[('1',''),('2',''),('3',''),('4',''),('5','')]))
	form = F(request.form)
	return render_template('form.html', form=form, error=error)

### END MAIN FORM ###

if __name__ == '__main__':
	app.run()