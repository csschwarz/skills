import unittest 
from flask.ext.testing import TestCase, Twill
from flask.ext.mongoengine import MongoEngine
from flask import Flask
from twill import get_browser
from twill.commands import *
import skills

class AdminTestCase(TestCase):

	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['SERVER_NAME'] = 'localhost:5001' 
		app.config['MONGODB_DB'] = 'hacksaw_testdb'
		return app

	def setUp(self):
		pass

	def test_valid_admin_login(self):
		with Twill(self.app, host='localhost', port=5001) as t:		
			t.browser.go("http://localhost:5001/")  
			t.browser.showforms() 
			# formclear('1')
			# fv('1', 'username', 'admin')
			# fv('1', 'password', 'admin') 
			# submit()
			
			code(200)
			url("http://localhost:5000/admin/")
	
	def tearDown(self):
		pass

if __name__ == '__main__':
	unittest.main()
