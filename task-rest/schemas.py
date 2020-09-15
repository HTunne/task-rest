from marshmallow import Schema, fields, post_dump
from datetime import datetime


class TaskAnnotationSchema(Schema):
    description = fields.Str(required = True)
    entry = fields.DateTime(format="rfc", dump_only = True) # read-only

class TaskSchema(Schema):
    annotations = fields.List(fields.Nested(TaskAnnotationSchema), dump_only = True)
    depends = fields.List(fields.Nested(lambda: TaskSchema(exclude=("depends",))), dump_only = True)
    description = fields.Str(required = True)
    due = fields.DateTime(format="rfc")
    end = fields.DateTime(format="rfc", dump_only = True) # read-only
    entry = fields.DateTime(format="rfc", dump_only = True) # read-only
    id = fields.Int(dump_only=True) # read-only
    imask = fields.Int(dump_only=True) # read-only
    mask = fields.Str()
    modified = fields.DateTime(format="rfc", dump_only=True) # read-only
    parent = fields.Str(dump_only=True) # read-only
    priority = fields.Str()
    project = fields.Str()
    recur = fields.Str()
    scheduled = fields.DateTime(format="rfc")
    start = fields.DateTime(format="rfc")
    status = fields.Str(dump_only = True) # read-only
    tags = fields.List(fields.Str())
    until = fields.DateTime(format="rfc")
    urgency = fields.Float(dump_only= True) # read-only
    uuid = fields.Str(required = True, dump_only=True) # read-only

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

