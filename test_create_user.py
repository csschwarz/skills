import unittest
from skills.create_user import create_user
from skills.models import User
from flask import request
from minimock import Mock
from wtforms import Form

class SkillsTestCase(unittest.TestCase):

	def test_should_create_valid_user(self):
		form = Mock('Form')
		user_class = Mock('User')
		user_class.objects = Mock('')
		user_class.objects.count =

		assert "some url" == create_user(form, user_class, 'username')

if __name__ == '__main__':
	unittest.main()