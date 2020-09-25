from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from tasklib import TaskWarrior, Task

from task_rest.config import ProductionConfig, DevelopmentConfig
from task_rest.resources import TaskResource, TaskListResource, TaskCommandResource, AuthResource

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    if app.config["ENV"] == "production":
        app.config.from_object(ProductionConfig())
    else:
        app.config.from_object(DevelopmentConfig())

    CORS(app)
    tw = TaskWarrior(
        data_location=app.config['TASKDATA_LOCATION'],
        taskrc_location=app.config['TASKRC_LOCATION']
    )

    api = Api(app)
    api.add_resource(AuthResource, '/auth')
    api.add_resource(TaskListResource, '/', resource_class_args=(tw,))
    api.add_resource(TaskResource, '/<string:task_uuid>', resource_class_args=(tw,))
    api.add_resource(TaskCommandResource,
                     '/<string:task_uuid>/<string:command>',
                     resource_class_args=(tw,))

    return app
