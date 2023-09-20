import os

from requests import Response, post  # type: ignore


def notify(
    task_id: str,
    result: str,
    data: dict | None,  # type: ignore
) -> Response:
    return post(
        "http://task_manager:{}/api/tasks/{}/{}/".format(
            os.environ.get("INTERNAL_TASK_MANAGER_PORT"),
            task_id,
            result,
        ),
        json=data,
    )


def success(
    task_id: str,
    data: dict | None = None,  # type: ignore
) -> Response:
    return notify(task_id, "success", data=data)


def error(
    task_id: str,
    data: dict | None = None,  # type: ignore
) -> Response:
    return notify(task_id, "failed", data=data)
