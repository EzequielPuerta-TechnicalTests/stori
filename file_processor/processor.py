import csv
import os

from celery import Celery
from src.summary import Summary, Transaction

app = Celery(
    "task_manager",
    broker="pyamqp://user:bitnami@rabbitmq",
    backend="rpc://user:bitnami@rabbitmq",
)


@app.task(name="pendings")
def process_file_named(file_name: str, task_id: str) -> None:
    file_path = os.path.join(os.sep, "input", file_name)
    with open(file_path, "r") as transactions_file:
        lines = csv.reader(
            transactions_file,
        )
        next(lines, None)  # Ignore csv headers
        transactions = map(lambda line: Transaction.related_to(*line), lines)
        result = sum(transactions, Summary())
        print(result)
