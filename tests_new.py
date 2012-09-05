import unittest 
from flask.ext.testing import TestCase, Twill
from flask.ext.mongoengine import MongoEngine
from flask import Flask
import skills

class SkillsTestCase(TestCase):

	def create_app(self):
		app = Flask(__name__)
		app.config['TESTING'] = True
		app.config['MONGODB_DB'] = 'hacksaw_testdb'
		return app

	def setUp(self):
		pass

	def test_something(self):
		with Twill(self.app, host='localhost', port=5000) as t:
			t.browser.go(t.url("/"))
	
	def tearDown(self):
		pass 

if __name__ == '__main__':
	unittest.main()
