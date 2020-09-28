from functools import wraps
from flask import current_app
from flask import jsonify, request, make_response
from flask_restful import Resource
from tasklib import Task
from tasklib.backends import TaskWarriorException
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import jwt

from task_rest.schemas import TaskSchema, TaskAnnotationSchema, DependantTaskSchema

ts = TaskSchema(unknown='EXCLUDE')
tas = TaskAnnotationSchema(unknown='EXCLUDE')
dts = DependantTaskSchema(unknown='EXCLUDE')


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

def expose_errors(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        except TaskWarriorException as e:
            error = '\n'.join([x for x in str(e).split('\n') if not (
                x.startswith("Configuration override")
                or x.startswith("Command used")
                or x.startswith("TASKRC")
                or x.startswith("TASKDATA")
            )])
            result = jsonify({'message': {
                'description': error,
                'type': 'error'
            }})
        return result
    return decorator

def json_task_and_message(task, message, msg_type):
    return jsonify({
        'task': ts.dump(task),
        'message': {
            'description': message.format(task['id']),
            'type': msg_type
        }
    })


class TaskResource(Resource):
    def __init__(self, tw):
        self.tw = tw

    method_decorators = [token_required, expose_errors]
    def get(self, task_uuid):
        task = self.tw.tasks.get(uuid = task_uuid)
        return jsonify({'task': ts.dump(task)})

    # task modify
    def put(self, task_uuid):
        task = self.tw.tasks.get(uuid = task_uuid)
        data = ts.loads(request.data)
        for key in data:
            task[key] = data[key]
        task.save()
        return json_task_and_message(task, 'Modified task {}.', 'success')

    # task delete
    def delete(self, task_uuid):
        task = self.tw.tasks.get(uuid = task_uuid)
        task.delete()
        return json_task_and_message(task, 'Deleted task {}.', 'info')


class TaskListResource(Resource):
    def __init__(self, tw):
        self.tw = tw

    method_decorators = [token_required, expose_errors]
    def get(self):
        return jsonify({'tasks': ts.dump(self.tw.tasks.all(), many=True)})

    def post(self):
        task = Task(self.tw)
        data = ts.loads(request.data)
        for key in data:
            task[key] = data[key]
        task.save()
        return json_task_and_message(task, 'Added task {}.', 'success')


class TaskCommandResource(Resource):
    def __init__(self, tw):
        self.tw = tw

    method_decorators = [token_required, expose_errors]
    def put(self, task_uuid, command):
        task = self.tw.tasks.get(uuid = task_uuid)
        if command == 'done':
            msg = 'Completed task {}.'
            task.done()
        elif command == 'restore':
            msg = 'Restored task {}.'
            task['status'] = 'pending'
            task.save()
        elif command == 'start':
            msg = 'Started task {}.'
            task.start()
        elif command == 'stop':
            msg = 'Stopped task {}.'
            task.stop()
        elif command == 'add_annotation':
            msg = 'Added annotation to task {}.'
            data = tas.loads(request.data)
            task.add_annotation(data["description"])
        elif command == 'remove_annotation':
            msg = 'Removed annotaion from task {}'
            data = tas.loads(request.data)
            task.remove_annotation(data["description"])
        elif command == 'add_dependency':
            msg = 'Added dependency to task {}'
            data = dts.loads(request.data)
            dep = self.tw.tasks.get(uuid = data['uuid'])
            task['depends'].add(dep)
            task.save()
        elif command == 'remove_dependency':
            msg = 'Removed dependency to task {}'
            data = dts.loads(request.data)
            dep = self.tw.tasks.get(uuid = data['uuid'])
            task['depends'].remove(dep)
            task.save()
        return json_task_and_message(task, msg, 'info')


class TaskServerResource(Resource):
    def __init__(self, tw):
        self.tw = tw

    method_decorators = [token_required, expose_errors]
    def get(self):
        self.tw.sync()
        return jsonify({
            'message': {
                'description': 'Sync successful.',
                'type': 'info'
            }
        })


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
