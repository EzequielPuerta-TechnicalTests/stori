import json
import os

import pytest
from api.app import create_app
from api.database import initialize_mongodb, mongo
from flask.testing import FlaskClient


@pytest.fixture
def app_client() -> FlaskClient:
    database_name = f"{os.environ['MONGODB_DATABASE']}_test"
    _app = create_app(database_name)
    initialize_mongodb(_app)

    @_app.route("/")
    def home():  # type: ignore
        return "Flask client for tests"

    yield _app.test_client()
    mongo.db.client.drop_database(database_name)


@pytest.fixture
def post_new_task(app_client):  # type: ignore
    task_data = {
        "customer_id": 1,
        "file_name": "myFile.csv",
    }
    response = app_client.post("/api/tasks/", json=task_data)
    yield json.loads(response.data.decode("utf-8"))


@pytest.fixture
def task_done(app_client, post_new_task):  # type: ignore
    _id = post_new_task["_id"]
    for i in range(1, 4):
        response = app_client.post(f"/api/tasks/{_id}/success")
    yield json.loads(response.data.decode("utf-8"))


@pytest.fixture
def task_failed(app_client, post_new_task):  # type: ignore
    _id = post_new_task["_id"]
    response = app_client.post(f"/api/tasks/{_id}/failed")
    yield json.loads(response.data.decode("utf-8"))
