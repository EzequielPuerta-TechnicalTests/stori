import os

from requests import Response, post  # type: ignore


def notify(task_id: str, result: str) -> Response:
    return post(
        "http://task_manager:{}/api/tasks/{}/{}".format(
            os.environ.get("INTERNAL_TASK_MANAGER_PORT"),
            task_id,
            result,
        )
    )


def success(task_id: str) -> Response:
    return notify(task_id, "success")


def error(task_id: str) -> Response:
    return notify(task_id, "failed")
