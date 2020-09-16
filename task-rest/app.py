from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_marshmallow import Marshmallow

from resources import TaskResource, TaskListResource, TaskCommandResource

app = Flask(__name__)
api = Api(app)
ma = Marshmallow(app)

CORS(app, resources={r'/*': {'origins': '*'}})
api.add_resource(TaskListResource, '/')
api.add_resource(TaskResource, '/<string:task_uuid>')
api.add_resource(TaskCommandResource, '/<string:task_uuid>/<string:command>')

if __name__ == "__main__":
    app.run(debug=True)
