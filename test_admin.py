import unittest 
from flask.ext.testing import TestCase, Twill
from flask.ext.mongoengine import MongoEngine
from flask import Flask
from skills import create_app
import dbinit

class AdminTestCase(TestCase):

	BASE_URL = 'http://127.0.0.1:5001'
	ADMIN_URL = BASE_URL + '/admin/'

	def create_app(self):
		return create_app('test_config.py')

	def setUp(self):
		dbinit.drop_all()
		dbinit.seed()

	def test_invalid_login(self):
		resp = self.login('fakeuser', 'fakepass')
		assert 'Invalid' in resp

	def test_view_all_users_with_java(self):
		self.login('admin', 'admin')

	def login(self, username, password):
		return self.client.post('/', data=dict(
			username=username,
			password=password
		), follow_redirects=True)

if __name__ == '__main__':
	unittest.main()
