import csv
import os

import notifier as notify
import src.core_client as core
from celery import Celery
from src.summary import Summary, Transaction

app = Celery(
    "task_manager",
    broker="pyamqp://user:bitnami@rabbitmq",
    backend="rpc://user:bitnami@rabbitmq",
)


def get_summary_from(lines) -> Summary:  # type: ignore
    trxs = map(lambda line: Transaction.related_to(*line), lines)
    return sum(trxs, Summary())  # type: ignore


def process_file(file_path: str, task_id: str) -> None:
    with open(file_path, "r") as file:
        notify.success(task_id)
        lines = csv.reader(file)
        next(lines, None)  # Ignore csv headers
        summary = get_summary_from(lines)
        file_name = os.path.basename(file_path).split("_")[0]
        account = core.Client.accounts().get(_params={"alias": file_name})
        print(account)
        print(str(account))
        print(repr(account))
        account = account.json()[0]

        summary_data = {
            "total_balance": summary.total_balance,
            "average_debit_amount": summary.average_debit_amount,
            "average_credit_amount": summary.average_credit_amount,
            "account": account["url"],
            "transactions": [],
        }

        summary_result = core.Client.summaries().post(summary_data).json()
        transactions = [
            {
                "provider_id": transaction.provider_id,
                "day": transaction.day,
                "month": transaction.month,
                "amount": transaction.signed_amount,
                "summary": summary_result["url"],
            }
            for transaction in summary.transactions
        ]

        core.Client.transactions().post(transactions)


@app.task(name="pendings")
def process(file_name: str, task_id: str) -> None:
    file_path = os.path.join(os.sep, "input", file_name)
    try:
        process_file(file_path, task_id)
        notify.success(task_id)
    except (FileNotFoundError, KeyError):
        notify.error(task_id)
