import unittest 
from flask.ext.testing import TestCase, Twill
from flask.ext.mongoengine import MongoEngine
from flask import Flask
from skills import create_app
import dbinit

class AdminTestCase(TestCase):

	def create_app(self):
		return create_app('test_config.py')

	def setUp(self):
		dbinit.drop_all()
		dbinit.seed()

	def test_invalid_login(self):
		resp = self.login('fake', 'fake')
		assert '<p class="error"><strong>Error:</strong> Invalid' in resp.data

	def test_blank_login_fails(self):
		resp = self.login()
		assert '<p class="error"><strong>Error:</strong> Can' in resp.data

	def test_admin_console(self):
		resp = self.login('admin', 'admin', 'Admin')
		self._view_all_users_with_skill_java(resp)
		self._view_single_user_skills()

	def _view_all_users_with_skill_java(self, resp):
		resp = self.client.get('/admin/viewskill/Java')
		assert 'Test User' in resp.data

	def _view_single_user_skills(self):
		resp = self.client.get('/admin/viewuser/test')
		assert 'Java' in resp.data

	def login(self, username='', password='', title=None):
		resp = self.client.post('/', data=dict(
			username=username,
			password=password
		), follow_redirects=True)
		if title:
			assert '<title>Hacksaw - '+title+'</title>' in resp.data
		return resp

if __name__ == '__main__':
	unittest.main()
