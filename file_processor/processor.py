import csv
import os

from celery import Celery
from requests import Response, post  # type: ignore
from src.summary import Summary, Transaction

app = Celery(
    "task_manager",
    broker="pyamqp://user:bitnami@rabbitmq",
    backend="rpc://user:bitnami@rabbitmq",
)


def notify(task_id: str, result: str) -> Response:
    return post(
        "http://task_manager:{}/api/tasks/{}/{}".format(
            os.environ.get("INTERNAL_TASK_MANAGER_PORT"),
            task_id,
            result,
        )
    )


def notify_success(task_id: str) -> Response:
    return notify(task_id, "success")


def notify_error(task_id: str) -> Response:
    return notify(task_id, "failed")


def get_summary_from(lines) -> Summary:  # type: ignore
    trxs = map(lambda line: Transaction.related_to(*line), lines)
    return sum(trxs, Summary())  # type: ignore


@app.task(name="pendings")
def process_file_named(file_name: str, task_id: str) -> None:
    file_path = os.path.join(os.sep, "input", file_name)
    try:
        with open(file_path, "r") as transactions_file:
            if notify_success(task_id).ok:
                lines = csv.reader(transactions_file)
                next(lines, None)  # Ignore csv headers
                summary = get_summary_from(lines)

                if notify_success(task_id).ok:
                    print(
                        "File {} processed by task {}: {}".format(
                            file_name,
                            task_id,
                            summary,
                        )
                    )
    except FileNotFoundError:
        notify_error(task_id)
