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
		resp = self.login('fakeuser', 'fakepass')
		assert '<p class="error"><strong>Error:</strong> Invalid' in resp.data

	def test_view_all_users_with_java(self):
		resp = self.login('admin', 'admin')
		assert '<title>Hacksaw - Admin</title>' in resp.data
		resp = self.client.get('/admin/viewskill/Java')
		assert 'Test User' in resp.data

	def test_view_single_user(self):
		self.login('admin', 'admin')
		resp = self.client.get('/admin/viewuser/test')
		assert 'Java' in resp.data

	def login(self, username, password):
		return self.client.post('/', data=dict(
			username=username,
			password=password
		), follow_redirects=True)

if __name__ == '__main__':
	unittest.main()
