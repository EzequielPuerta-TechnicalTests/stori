import csv

from celery import Celery

app = Celery(
    "task_manager",
    broker="pyamqp://user:bitnami@rabbitmq",
    backend="rpc://user:bitnami@rabbitmq",
)


@app.task(name="pendings")
def process_file_named(file_name: str) -> None:
    with open(file_name, "r") as transactions_file:
        for transaction_line in csv.reader(transactions_file):
            print(transaction_line)
