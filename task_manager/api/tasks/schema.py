from typing import Any

from api.tasks.task import Task
from marshmallow import Schema, fields, post_load


class TaskSchema(Schema):
    _id = fields.Str()
    customer_id = fields.Int()
    file_name = fields.Str()
    status = fields.Str()

    @post_load
    def make(self, data: Any, **kwargs: Any) -> Task:
        return Task(**data)
