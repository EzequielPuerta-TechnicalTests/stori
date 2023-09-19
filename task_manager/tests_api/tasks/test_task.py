import uuid

import api.tasks.status as s
from api.exceptions import InvalidStateTransition
from api.tasks.task import Task
from pytest import raises as pytest_raises


def test_task_creation() -> None:
    task = Task(123, "myFile.csv")
    assert task.customer_id == 123
    assert task.file_name == "myFile.csv"
    assert task.status == s.PENDING
    assert task._id is not None


def test_task_with_id_creation() -> None:
    identifier = uuid.uuid4().hex
    task = Task(123, "myFile.csv", _id=identifier)
    assert task.customer_id == 123
    assert task.file_name == "myFile.csv"
    assert task.status == s.PENDING
    assert task._id == identifier


def test_pending_task_transitions() -> None:
    task1 = Task(123, "myFile1.csv")
    task2 = Task(456, "myFile2.csv")

    assert task1.status == s.PENDING
    task1.state_transition(success=True)
    assert task1.status == s.IN_PROGRESS

    assert task2.status == s.PENDING
    task2.state_transition(success=False)
    assert task2.status == s.FILE_ERROR


def test_in_progress_task_transitions() -> None:
    task1 = Task(123, "myFile1.csv", status=s.IN_PROGRESS)
    task2 = Task(456, "myFile2.csv", status=s.IN_PROGRESS)

    assert task1.status == s.IN_PROGRESS
    task1.state_transition(success=True)
    assert task1.status == s.EMAIL_PENDING

    assert task2.status == s.IN_PROGRESS
    task2.state_transition(success=False)
    assert task2.status == s.TRANSACTION_ERROR


def test_email_pending_task_transitions() -> None:
    task1 = Task(123, "myFile1.csv", status=s.EMAIL_PENDING)
    task2 = Task(456, "myFile2.csv", status=s.EMAIL_PENDING)

    assert task1.status == s.EMAIL_PENDING
    task1.state_transition(success=True)
    assert task1.status == s.DONE

    assert task2.status == s.EMAIL_PENDING
    task2.state_transition(success=False)
    assert task2.status == s.EMAIL_ERROR


def test_invalid_task_transitions() -> None:
    for status in s.TERMINALS:
        for result in [s.SUCCESS, s.FAILED]:
            with pytest_raises(InvalidStateTransition) as error:
                task = Task(123, "myFile1.csv", status=status)
                task.state_transition(result)
            assert "Unexpected state transition request." in str(error.value)
