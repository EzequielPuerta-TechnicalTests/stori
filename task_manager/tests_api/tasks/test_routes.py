import codecs
import json

import api.tasks.status as s

reader = codecs.getreader("utf-8")


def test_app_creation(app_client) -> None:  # type: ignore
    response = app_client.get("/")
    assert response.status_code == 200
    assert b"Flask client for tests" in response.data


def test_api_empty_tasks(app_client) -> None:  # type: ignore
    response = app_client.get("/api/tasks/")
    tasks = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert len(tasks) == 0


def test_api_task_creation(app_client) -> None:  # type: ignore
    task_data = {
        "customer_id": 1,
        "file_name": "myFile.csv",
    }
    response = app_client.post("/api/tasks/", json=task_data)
    task = json.loads(response.data.decode("utf-8"))

    assert response.status_code == 201
    assert task["_id"] is not None
    assert task["customer_id"] == 1
    assert task["file_name"] == "myFile.csv"
    assert task["status"] == s.PENDING


def test_api_tasks(app_client) -> None:  # type: ignore
    response = app_client.get("/api/tasks/")
    tasks = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert len(tasks) == 0

    task_data = {
        "customer_id": 1,
        "file_name": "myFile.csv",
    }
    response = app_client.post("/api/tasks/", json=task_data)
    task = json.loads(response.data.decode("utf-8"))

    response = app_client.get("/api/tasks/")
    tasks = json.loads(response.data.decode("utf-8"))
    assert response.status_code == 200
    assert len(tasks) == 1
    assert tasks == [task]


def test_get_task(app_client, post_new_task) -> None:  # type: ignore
    response = app_client.get(f"/api/tasks/{post_new_task['_id']}")
    assert response.status_code == 200

    get_task_data = json.loads(response.data.decode("utf-8"))
    assert post_new_task["_id"] == get_task_data["_id"]
    assert post_new_task["customer_id"] == get_task_data["customer_id"]
    assert post_new_task["file_name"] == get_task_data["file_name"]
    assert post_new_task["status"] == get_task_data["status"]


def test_get_task_with_wrong_id(app_client) -> None:  # type: ignore
    response = app_client.get("/api/tasks/")
    tasks = json.loads(response.data.decode("utf-8"))
    assert len(tasks) == 0

    response = app_client.get("/api/tasks/wrongID")
    message = json.loads(response.data.decode("utf-8"))["message"]
    assert "Task not found" in message


def test_notify_successful_state(  # type: ignore
    app_client,
    post_new_task,
) -> None:
    assert post_new_task["status"] == s.PENDING

    _id = post_new_task["_id"]
    response = app_client.post(f"/api/tasks/{_id}/success")
    assert response.status_code == 200

    task_data = json.loads(response.data.decode("utf-8"))
    assert post_new_task["_id"] == task_data["_id"]
    assert post_new_task["customer_id"] == task_data["customer_id"]
    assert post_new_task["file_name"] == task_data["file_name"]
    assert not post_new_task["status"] == task_data["status"]
    assert post_new_task["status"] == s.PENDING
    assert task_data["status"] == s.IN_PROGRESS


def test_notify_failed_state(  # type: ignore
    app_client,
    post_new_task,
) -> None:
    assert post_new_task["status"] == s.PENDING

    _id = post_new_task["_id"]
    response = app_client.post(f"/api/tasks/{_id}/failed")
    assert response.status_code == 200

    task_data = json.loads(response.data.decode("utf-8"))
    assert post_new_task["_id"] == task_data["_id"]
    assert post_new_task["customer_id"] == task_data["customer_id"]
    assert post_new_task["file_name"] == task_data["file_name"]
    assert not post_new_task["status"] == task_data["status"]
    assert post_new_task["status"] == s.PENDING
    assert task_data["status"] == s.FILE_ERROR


def test_notify_successful_state_with_wrong_id(  # type: ignore
    app_client,
) -> None:
    response = app_client.get("/api/tasks/")
    tasks = json.loads(response.data.decode("utf-8"))
    assert len(tasks) == 0

    response = app_client.post("/api/tasks/wrongID/success")
    assert response.status_code == 200
    message = json.loads(response.data.decode("utf-8"))["message"]
    assert "Task not found" in message


def test_notify_failed_state_with_wrong_id(app_client) -> None:  # type: ignore
    response = app_client.get("/api/tasks/")
    tasks = json.loads(response.data.decode("utf-8"))
    assert len(tasks) == 0

    response = app_client.post("/api/tasks/wrongID/failed")
    assert response.status_code == 200
    message = json.loads(response.data.decode("utf-8"))["message"]
    assert "Task not found" in message


def test_complete_successful_state_transition(  # type: ignore
    app_client, post_new_task
) -> None:
    assert post_new_task["status"] == s.PENDING
    _id = post_new_task["_id"]

    response = app_client.post(f"/api/tasks/{_id}/success")
    task_data = json.loads(response.data.decode("utf-8"))
    assert task_data["status"] == s.IN_PROGRESS

    response = app_client.post(f"/api/tasks/{_id}/success")
    task_data = json.loads(response.data.decode("utf-8"))
    assert task_data["status"] == s.EMAIL_PENDING

    response = app_client.post(f"/api/tasks/{_id}/success")
    task_data = json.loads(response.data.decode("utf-8"))
    assert task_data["status"] == s.DONE


def test_notify_task_when_its_done(  # type: ignore
    app_client,
    task_done,
) -> None:
    assert task_done["status"] == s.DONE
    _id = task_done["_id"]

    response = app_client.post(f"/api/tasks/{_id}/success")
    assert response.status_code == 200
    message = json.loads(response.data.decode("utf-8"))["message"]
    assert "Unexpected state transition request." in message

    response = app_client.post(f"/api/tasks/{_id}/failed")
    assert response.status_code == 200
    message = json.loads(response.data.decode("utf-8"))["message"]
    assert "Unexpected state transition request." in message


def test_notify_task_when_its_failed(  # type: ignore
    app_client,
    task_failed,
) -> None:
    assert task_failed["status"] == s.FILE_ERROR
    _id = task_failed["_id"]

    response = app_client.post(f"/api/tasks/{_id}/success")
    assert response.status_code == 200
    message = json.loads(response.data.decode("utf-8"))["message"]
    assert "Unexpected state transition request." in message

    response = app_client.post(f"/api/tasks/{_id}/failed")
    assert response.status_code == 200
    message = json.loads(response.data.decode("utf-8"))["message"]
    assert "Unexpected state transition request." in message
