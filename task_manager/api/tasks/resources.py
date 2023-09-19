from api.database import mongo
from api.exceptions import ResourceNotFound
from api.tasks.schema import TaskSchema
from celery import Celery
from flask import request
from flask_restful import Resource

task_schema = TaskSchema()
event_broker = Celery(
    "task_manager",
    broker="pyamqp://user:bitnami@rabbitmq",
    backend="rpc://user:bitnami@rabbitmq",
)


class TaskListResource(Resource):
    def get(self):  # type: ignore
        tasks = mongo.db.tasks.find()
        return task_schema.dump(tasks, many=True)

    def post(self):  # type: ignore
        data = request.get_json()
        task = task_schema.load(data)
        task_data = task_schema.dump(task)
        mongo.db.tasks.insert_one(task_data)
        event_broker.send_task(
            "pendings",
            (
                task_data["file_name"],
                task_data["_id"],
            ),
        )
        return task_data, 201


class TaskResource(Resource):
    def get(self, task_id: str):  # type: ignore
        task = mongo.db.tasks.find_one({"_id": task_id})
        if task is None:
            raise ResourceNotFound("Task not found.")
        return task_schema.dump(task)


class TaskStateResource(Resource):
    def post(self, task_id: str, success: bool):  # type: ignore
        task_data = mongo.db.tasks.find_one({"_id": task_id})
        if task_data is None:
            raise ResourceNotFound("Task not found.")
        task = task_schema.load(task_data)
        task.state_transition(success)
        task_data = task_schema.dump(task)
        mongo.db.tasks.update_one({"_id": task_id}, {"$set": task_data})
        return task_data, 200


class SuccessfulTaskStateResource(TaskStateResource):
    def post(self, task_id: str):  # type: ignore
        return super().post(task_id, True)


class FailedTaskStateResource(TaskStateResource):
    def post(self, task_id: str):  # type: ignore
        return super().post(task_id, False)
