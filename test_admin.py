import unittest 
from flask.ext.testing import TestCase, Twill
from flask.ext.mongoengine import MongoEngine
from flask import Flask
from twill import get_browser
from twill.commands import *
from skills import create_app
import dbinit

class AdminTestCase(TestCase):

	def create_app(self):
		return create_app('test_config.py')

	def setUp(self):
		dbinit.drop_all()
		dbinit.seed()

	def test_valid_admin_login(self):
		self.login('admin', 'admin')
		with Twill(self.app, port=5001) as t:
			code(200)
			url("http://127.0.0.1:5001/admin/")

	def test_valid_normal_login(self):
		self.login('test', 't')
		with Twill(self.app, port=5001) as t:
			code(200)
			url('http://127.0.0.1:5001/form/0')

	def test_invalid_login(self):
		self.login('fakeuser', 'fakepass')
		with Twill(self.app, port=5001) as t:
			url('http://127.0.0.1:5001/')
	
	def tearDown(self):
		pass

	def login(self, username, password):
		with Twill(self.app, port=5001) as t:
			t.browser.go(t.url('/'))
			showforms()
			formclear('1')
			fv('1', 'username', username)
			fv('1', 'password', password)
			submit()

if __name__ == '__main__':
	unittest.main()
