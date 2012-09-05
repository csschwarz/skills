import unittest 
from flask.ext.testing import TestCase, Twill
from flask.ext.mongoengine import MongoEngine
from flask import Flask
from twill import get_browser
from twill.commands import *
from skills import create_app

class AdminTestCase(TestCase):

	def create_app(self):
		return create_app('test_config.py')

	def setUp(self):
		pass

	def test_valid_admin_login(self):
		with Twill(self.app, port=5000) as t:
			t.browser.go(t.url("/"))	  
			showforms() 
			formclear('1')
			fv('1', 'username', 'admin')
			fv('1', 'password', 'admin') 
			submit()
			
			code(200)
			url("http://localhost:5000/admin/")
	
	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()
