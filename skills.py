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
	if session.get('username') and session.get('isadmin'):
		return redirect(url_for('admin'))
	elif session.get('username'):
		return redirect(url_for('form', pagenum=0))
	if request.method == 'POST' and form.validate():
		user = query_db('select * from user where username=? and password=?', 
				[request.form['username'], request.form['password']], one=True)
		if not user is None:
			session['username'] = request.form['username']
			session.pop('isadmin', None)
			flash('Login successful!')
			if user['isadmin']:
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
		if pagenum < len(categories)-1:
			return redirect(url_for('form', pagenum=pagenum+1))
		else:
			return redirect(url_for('logout'))
	elif request.method == 'POST':
		error = "You didn't fill out the whole form. Please do that."
	return render_template('form.html', form=form, categories=categories, pagenum=pagenum, scoredesc=scoredesc, error=error)

### END MAIN FORM ###
### BEGIN ADMIN ###

@app.route('/admin/')
def admin():
	if not session.get('isadmin'):
		abort(401)
	users = query_db('select id, username, firstname, lastname from user where id in \
			(select distinct userid from userskill) order by lastname')
	allskills = query_db('select name, category from skilltab order by category, name')
	return render_template('admin_index.html', users=users, allskills=allskills)

@app.route('/admin/viewuser/<int:userid>')
def admin_userstats(userid):
	if not session.get('isadmin'):
		abort(401)
	scoredesc = {elem['score']: elem['description'] for elem in query_db('select * from scoredescription order by score')}
	user = query_db('select * from user where id=?', [userid], one=True)
	categories = [item['category'] for item in query_db('select category from skilltab group by category order by category')]
	skills = dict()
	for category in categories:
		skills[category] = query_db('select u.skill, u.score from userskill as u \
				join skilltab as s on u.skill=s.name where u.userid=? and s.category=? order by u.score desc', [userid, category])
	return render_template('admin_userstats.html', user=user, skills=skills, categories=categories, scoredesc=scoredesc)

@app.route('/admin/viewskill/<skill>')
def admin_skillstats(skill):
	if not session.get('isadmin'):
		abort(401)
	scoredesc = {elem['score']: elem['description'] for elem in query_db('select * from scoredescription order by score')}
	users = query_db('select u.id, u.firstname, u.lastname, us.score from user as u \
			join userskill as us on u.id=us.userid \
			where us.skill=? order by us.score desc', [skill])
	return render_template('admin_skillstats.html', skillname=skill, users=users, scoredesc=scoredesc)

### END ADMIN ###

if __name__ == '__main__':
	app.run()