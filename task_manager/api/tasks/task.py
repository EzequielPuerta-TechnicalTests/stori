import uuid

from api.tasks.status import PENDING, STATUS


class Task:
    def __init__(self, customer_id: int, file_name: str, _id: str = None):
        self._id = _id or uuid.uuid4().hex
        self.customer_id: int = customer_id
        self.file_name: str = file_name
        self.status: STATUS = PENDING
