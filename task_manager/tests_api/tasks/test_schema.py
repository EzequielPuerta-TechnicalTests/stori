import uuid

from api.tasks.schema import TaskSchema
from api.tasks.status import PENDING
from api.tasks.task import Task


def test_task_schema_dump() -> None:
    identifier = uuid.uuid4().hex
    task = Task(123, "myFile.csv", _id=identifier)
    schema = TaskSchema().dump(task)

    assert schema["_id"] == identifier
    assert schema["customer_id"] == 123
    assert schema["file_name"] == "myFile.csv"
    assert schema["status"] == PENDING


def test_task_schema_load() -> None:
    task_data = {
        "_id": "6b254cbcd43b437987fbcb2f0c333c26",
        "customer_id": 123,
        "file_name": "myFile.csv",
        "status": "pending",
    }
    task = TaskSchema().load(task_data)

    assert task._id == "6b254cbcd43b437987fbcb2f0c333c26"
    assert task.customer_id == 123
    assert task.file_name == "myFile.csv"
    assert task.status == PENDING
