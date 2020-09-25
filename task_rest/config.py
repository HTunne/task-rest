from flask import Flask
from os import urandom
from os.path import join
import json
from werkzeug.security import generate_password_hash

app = Flask(__name__, instance_relative_config=True)
class Config(object):
    """Base config."""
    DEBUG = False
    TESTING = False
    TASKDATA_LOCATION = "~/.task"
    TASKRC_LOCATION = "~/.taskrc"


class ProductionConfig(Config):
    SECRET_KEY = urandom(16)
    def __init__(self):
        with app.open_instance_resource('config.json') as f:

            conf_dict = json.load(f)
            for key, value in conf_dict.items():
                setattr(self, key, value)

class DevelopmentConfig(Config):
    DEBUG = True
    TOKEN_EXP = 999
    PASSWORD = generate_password_hash('password', method='sha256')
    SECRET_KEY = 'SECRET_KEY'
    CORS_ORIGINS = '*'
    TASKDATA_LOCATION = join(app.instance_path, "dev", ".task")
    TASKRC_LOCATION = join(app.instance_path, "dev", ".taskrc")
