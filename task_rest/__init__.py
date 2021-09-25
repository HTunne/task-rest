from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from tasklib import TaskWarrior

from task_rest.config import ProductionConfig, DevelopmentConfig
from task_rest.resources import (TaskResource, TaskListResource,
                                 TaskCommandResource, TaskServerResource,
                                 AuthResource)

from os.path import join

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    if app.config["ENV"] == "production":
        app.config.from_object(ProductionConfig())
    else:
        app.config.from_object(DevelopmentConfig())

    print(app.config)

    CORS(app)

    api = Api(app)
    api.add_resource(AuthResource, '/auth')
    api.add_resource(TaskListResource, '/')
    api.add_resource(TaskResource, '/<string:task_uuid>')
    api.add_resource(TaskServerResource, '/sync')
    api.add_resource(TaskCommandResource, '/<string:task_uuid>/<string:command>')

    return app
