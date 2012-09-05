from create_app import create_app 
from flask.ext.mongoengine import MongoEngine 

app = create_app('app_config.py') 
db = MongoEngine(app) 

import skills.login
import skills.forms
import skills.admin