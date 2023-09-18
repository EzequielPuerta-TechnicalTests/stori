from api.database import mongo
from api.exceptions import ResourceNotFound
from api.tasks.schema import TaskSchema
from flask import request
from flask_restful import Resource

task_schema = TaskSchema()


class TaskListResource(Resource):
    def get(self):
        tasks = mongo.db.tasks.find()
        return task_schema.dump(tasks, many=True)

    def post(self):
        data = request.get_json()
        task = task_schema.load(data)
        task_data = task_schema.dump(task)
        mongo.db.tasks.insert_one(task_data)
        return task_data, 201


class TaskResource(Resource):
    def get(self, task_id):
        task = mongo.db.tasks.find_one({"_id": task_id})
        if task is None:
            raise ResourceNotFound("Task not found.")
        return task_schema.dump(task)


def initialize_routes(api):
    api.add_resource(
        TaskListResource,
        "/api/tasks/",
        endpoint="task_list_resource",
    )
    api.add_resource(
        TaskResource,
        "/api/tasks/<int:task_id>",
        endpoint="task_resource",
    )
