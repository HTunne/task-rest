from marshmallow import Schema, fields, post_dump
from datetime import datetime


class TaskAnnotationSchema(Schema):
    description = fields.Str(required = True)
    entry = fields.DateTime(format="rfc", dump_only = True) # read-only


class TaskSchema(Schema):
    description = fields.Str(required = True)
    due = fields.DateTime(format="rfc")
    priority = fields.Str()
    project = fields.Str()
    recur = fields.Str()
    scheduled = fields.DateTime(format="rfc")
    start = fields.DateTime(format="rfc")
    tags = fields.List(fields.Str())
    until = fields.DateTime(format="rfc")

    # read-only
    annotations = fields.List(fields.Nested(TaskAnnotationSchema), dump_only = True)
    depends = fields.List(fields.Nested(lambda: TaskSchema(exclude=("depends",))), dump_only = True)
    end = fields.DateTime(format="rfc", dump_only = True)
    entry = fields.DateTime(format="rfc", dump_only = True)
    id = fields.Int(dump_only=True)
    imask = fields.Int(dump_only=True)
    mask = fields.Str(dump_only=True)
    modified = fields.DateTime(format="rfc", dump_only=True)
    parent = fields.Str(dump_only=True)
    status = fields.Str(dump_only = True)
    urgency = fields.Float(dump_only= True)
    uuid = fields.Str(required = True, dump_only=True)

    @post_dump
    def remove_none_values(self, data, **kwargs):
        return {
            key: value for key, value in data.items() if value != None
        }

    @post_dump
    def remove_empty_lists(self, data, **kwargs):
        return {
            key: value for key, value in data.items() if ((type(value) is not list) or value)
        }



# used to add or remove dependancies, usually uuid is not deserialized
class DependantTaskSchema(Schema):
    uuid = fields.Str(required = True)
