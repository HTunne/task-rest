from flask import Flask
from os import urandom
import json
from werkzeug.security import generate_password_hash

app = Flask(__name__, instance_relative_config=True)
class Config(object):
    """Base config."""
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    SECRET_KEY = urandom(16)
    def __init__(self):
        with app.open_instance_resource('config.json') as f:

            conf_dict = json.load(f)
            for key, value in conf_dict.items():
                print(key)
                print(value)
                setattr(self, key, value)

class DevelopmentConfig(Config):
    DEBUG = True
    TOKEN_EXP = 999
    PASSWORD = generate_password_hash('password', method='sha256')
    SECRET_KEY = 'SECRET_KEY'
    ORIGIN = '*'
