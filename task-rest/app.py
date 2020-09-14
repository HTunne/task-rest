from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import reqparse, abort, fields, marshal_with, Api, Resource
from taskw import TaskWarrior


app = Flask(__name__)
api = Api(app)
w = TaskWarrior(marshal=True)

CORS(app, resources={r'/*': {'origins': '*'}})


def parse_date(value):
    return value

task_parser = reqparse.RequestParser()
task_parser.add_argument('description', type=str, help='Description could not be parsed.', required=True)
task_parser.add_argument('priority', type=str, choices=('H', 'M','L'),  help='Priority could not be parsed.')
task_parser.add_argument('project', type=str, help='Project could not be parsed.')
task_parser.add_argument('entry', type=parse_date, help='Entry date could not be parsed.')
task_parser.add_argument('start', type=parse_date, help='Start date could not be parsed.')
task_parser.add_argument('due', type=parse_date, help='Due date could not be parsed.')
task_parser.add_argument('tags', type=list, location='json', help='Tags could not be parsed.')
task_parser.add_argument('recurrence', type=str, help='Recurrence frequencycould not be parsed.')
task_parser.add_argument('until', type=parse_date, help='Until date could not be parsed.')
task_parser.add_argument('status', type=str, choices=('pending', 'completed'),  help='Until date could not be parsed.')


class Task(Resource):
    def get(self, task_uuid):
        return jsonify(w.get_task(uuid=task_uuid)[1])

    def put(self, task_uuid):
        id, task = w.get_task(uuid=task_uuid)
        args = {x:y for x,y in task_parser.parse_args().items() if y is not None}
        task.update(args)
        return jsonify(w.task_update(task)[1])

    def delete(self, task_uuid):
        return jsonify(w.task_delete(uuid=task_uuid))


class TaskList(Resource):
    def get(self):
        return jsonify(w.load_tasks())

    def post(self):
        print(request.args)
        args = {x:y for x,y in task_parser.parse_args().items() if y is not None}
        return jsonify(w.task_add(**args))

class TaskCommand(Resource):
    def put(self, task_uuid, command):
        print(command)
        if command == 'done':
            return jsonify(w.task_done(uuid=task_uuid))
        elif command == 'start':
            print('start')
            return jsonify(w.task_start(uuid=task_uuid))
        elif command == 'stop':
            return jsonify(w.task_stop(uuid=task_uuid))


api.add_resource(TaskList, '/')
api.add_resource(Task, '/<string:task_uuid>')
api.add_resource(TaskCommand, '/<string:task_uuid>/<string:command>')

if __name__ == "__main__":
    app.run(debug=True)
