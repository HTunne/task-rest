from os import urandom
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from werkzeug.security import generate_password_hash

from resources import TaskResource, TaskListResource, TaskCommandResource, AuthResource

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(16)
app.config['TOKEN_EXP'] = 30
app.config['PASSWORD'] = generate_password_hash('password', method='sha256')

CORS(app, resources={r'/*': {'origins': '*'}})

api = Api(app)
api.add_resource(AuthResource, '/auth')
api.add_resource(TaskListResource, '/')
api.add_resource(TaskResource, '/<string:task_uuid>')
api.add_resource(TaskCommandResource, '/<string:task_uuid>/<string:command>')

if __name__ == "__main__":
    app.run(debug=True)
