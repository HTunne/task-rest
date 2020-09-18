from functools import wraps
from flask import current_app
from flask import jsonify, request, make_response
from flask_restful import Resource
from tasklib import TaskWarrior, Task
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import jwt

from schemas import TaskSchema, TaskAnnotationSchema, DependantTaskSchema

ts = TaskSchema(unknown='EXCLUDE')
tas = TaskAnnotationSchema(unknown='EXCLUDE')
dts = DependantTaskSchema(unknown='EXCLUDE')
tw = TaskWarrior()


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        try:
            token = request.headers['x-access-tokens']
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
        except Exception as e:
            return make_response('Could not verify', 401, {'WWW.Authentification': 'Basic realm: "{}"'.format(e)})

        return f(*args, **kwargs)
    return decorator



class TaskResource(Resource):
    method_decorators = [token_required]
    def get(self, task_uuid):
        task = tw.tasks.get(uuid = task_uuid)
        return jsonify({'task': ts.dump(task)})

    def put(self, task_uuid):
        task = tw.tasks.get(uuid = task_uuid)
        data = ts.loads(request.data)
        for key in data:
            task[key] = data[key]
        task.save()
        return jsonify({'task': ts.dump(task)})

    def delete(self, task_uuid):
        task = tw.tasks.get(uuid = task_uuid)
        task.delete()
        return jsonify({'task': ts.dump(task)})


class TaskListResource(Resource):
    method_decorators = [token_required]
    def get(self):
        return jsonify({'tasks': ts.dump(tw.tasks.all(), many=True)})

    def post(self):
        task = Task(tw)
        data = ts.loads(request.data)
        for key in data:
            task[key] = data[key]
        task.save()
        return jsonify({'task': ts.dump(task)})


class TaskCommandResource(Resource):
    method_decorators = [token_required]
    def put(self, task_uuid, command):
        task = tw.tasks.get(uuid = task_uuid)
        if command == 'done':
            task.done()
        elif command == 'start':
            task.start()
        elif command == 'stop':
            task.stop()
        elif command == 'add_annotation':
            data = tas.loads(request.data)
            task.add_annotation(data["description"])
        elif command == 'remove_annotation':
            data = tas.loads(request.data)
            task.remove_annotation(data["description"])
        elif command == 'add_dependency':
            data = dts.loads(request.data)
            dep = tw.tasks.get(uuid = data['uuid'])
            task['depends'].add(dep)
            task.save()
        elif command == 'remove_dependency':
            data = dts.loads(request.data)
            dep = tw.tasks.get(uuid = data['uuid'])
            task['depends'].remove(dep)
            task.save()
        return jsonify({'task': ts.dump(task)})


class AuthResource(Resource):
    def get(self):
        auth = request.authorization
        if auth and auth.password and check_password_hash(current_app.config['PASSWORD'], auth.password):
            token = jwt.encode({
                'iat': datetime.utcnow(),
                'exp': datetime.utcnow() + timedelta(minutes=current_app.config['TOKEN_EXP'])
            }, current_app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('UTF-8')})
        return make_response('Could not verify', 401, {'WWW.Authentification': 'Basic realm: "login required"'})
