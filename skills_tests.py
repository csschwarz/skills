import os
import skills
import unittest
import tempfile
import flask

class SkillsTestCase(unittest.TestCase):

### BEGIN SETUP AND UTILS ###

	def setUp(self):
		self.db_fd, skills.app.config['DATABASE'] = tempfile.mkstemp()
		skills.app.config['TESTING'] = True
		self.app = skills.app.test_client()
		skills.init_db(test=True)

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(skills.app.config['DATABASE'])

	def login(self, username, password):
		return self.app.post('/', data=dict(
			username=username,
			password=password
		), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def with_normal_user(self):
		return self.login('default', 'd')

	def with_admin_user(self):
		return self.login('admin', 'admin')

### END SETUP AND UTILS ###
### BEGIN TESTS ###

	def test_nonadmin_login_logout(self):
		rv = self.with_normal_user()
		assert 'form action="/form' in rv.data
		rv = self.logout()
		assert 'You have been logged out.' in rv.data

	def test_admin_login_logout(self):
		rv = self.with_admin_user()
		assert 'All Users' in rv.data
		rv = self.logout()
		assert 'You have been logged out.' in rv.data

	def test_invalid_login(self):
		rv = self.login('bogus', 'fake')
		assert 'Invalid username or password' in rv.data

	def test_invalid_form_validation_fails(self):
		self.with_normal_user()
		rv = self.app.post('/form/0', data=dict(), follow_redirects=True)
		assert '<strong>Error:</strong> You didn&#39;t fill out the whole form' in rv.data
		self.logout()

	def test_valid_form_validation_succeeds(self):
		self.with_normal_user()
		rv = self.app.post('/form/0', data=dict(
			English=5,
			Portuguese=1,
			Spanish=3
		), follow_redirects=True)
		assert '/form/0' in rv.data
		self.logout()

### END TESTS ###

if __name__ == '__main__':
	unittest.main()