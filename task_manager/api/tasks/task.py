import uuid

from api.tasks.status import PENDING, STATUS, transition_from


class Task:
    def __init__(
        self,
        customer_id: int,
        file_name: str,
        _id: str | None = None,
        status: STATUS = PENDING,
    ):
        self._id = _id or uuid.uuid4().hex
        self.customer_id: int = customer_id
        self.file_name: str = file_name
        self.status: STATUS = status

    def state_transition(self, success: bool) -> None:
        self.status = transition_from(self.status, successful=success)
