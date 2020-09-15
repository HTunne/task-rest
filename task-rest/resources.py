from flask import jsonify, request
from flask_restful import Resource
from tasklib import TaskWarrior

from schemas import TaskSchema

ts = TaskSchema(unknown='EXCLUDE')
tw = TaskWarrior()

class Task(Resource):
    def get(self, task_uuid):
        task = tw.tasks.get(uuid = task_uuid)
        return jsonify(ts.dump(task))

    def put(self, task_uuid):
        task = tw.tasks.get(uuid = task_uuid)
        data = ts.loads(request.data)
        for key in data:
            task[key] = data[key]
        task.save()
        return jsonify(ts.dump(task))

    def delete(self, task_uuid):
        task = tw.tasks.get(uuid = task_uuid)
        task.delete()
        return jsonify(ts.dump(task))


class TaskList(Resource):
    def get(self):
        return jsonify(ts.dump(tw.tasks.all(), many=True))

    def post(self):
        task = Task(tw)
        data = ts.loads(request.data)
        for key in data:
            task[key] = data[key]
        task.save()
        return jsonify(ts.dump(task))

class TaskCommand(Resource):
    def put(self, task_uuid, command):
        print(command)
        if command == 'done':
            task = tw.tasks.get(uuid = task_uuid)
            task.done()
        elif command == 'start':
            task = tw.tasks.get(uuid = task_uuid)
            task.start()
        elif command == 'stop':
            task = tw.tasks.get(uuid = task_uuid)
            task.stop()
        return jsonify(ts.dump(task))



