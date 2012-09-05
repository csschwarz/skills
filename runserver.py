from skills import create_app
from flask.ext.mongoengine import MongoEngine

app = create_app('app_config.py')
app.run()