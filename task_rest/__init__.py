from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from task_rest.config import ProductionConfig, DevelopmentConfig
from task_rest.resources import TaskResource, TaskListResource, TaskCommandResource, AuthResource

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    if app.config["ENV"] == "production":
        app.config.from_object(ProductionConfig())
        print(app.config)
    else:
        app.config.from_object(DevelopmentConfig())

    CORS(app, resources={r'/*': {'origins': app.config['ORIGIN']}})

    api = Api(app)
    api.add_resource(AuthResource, '/auth')
    api.add_resource(TaskListResource, '/')
    api.add_resource(TaskResource, '/<string:task_uuid>')
    api.add_resource(TaskCommandResource, '/<string:task_uuid>/<string:command>')

    return app
