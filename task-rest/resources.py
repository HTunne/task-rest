from flask import jsonify, request
from flask_restful import Resource
from tasklib import TaskWarrior, Task

from schemas import TaskSchema, TaskAnnotationSchema, DependantTaskSchema

ts = TaskSchema(unknown='EXCLUDE')
tas = TaskAnnotationSchema(unknown='EXCLUDE')
dts = DependantTaskSchema(unknown='EXCLUDE')
tw = TaskWarrior()

class TaskResource(Resource):
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


class TaskListResource(Resource):
    def get(self):
        return jsonify(ts.dump(tw.tasks.all(), many=True))

    def post(self):
        task = Task(tw)
        data = ts.loads(request.data)
        for key in data:
            task[key] = data[key]
        task.save()
        return jsonify(ts.dump(task))

class TaskCommandResource(Resource):
    def put(self, task_uuid, command):
        print(command)
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
        return jsonify(ts.dump(task))



