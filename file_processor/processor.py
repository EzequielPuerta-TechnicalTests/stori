import csv
import os
import smtplib
from email.mime.text import MIMEText

import notifier as notify
import requests  # type: ignore
import src.core_client as core
from celery import Celery
from src.months import NAME_FOR
from src.summary import Summary, Transaction

app = Celery(
    "task_manager",
    broker="pyamqp://user:bitnami@rabbitmq",
    backend="rpc://user:bitnami@rabbitmq",
)


def get_summary_from(lines) -> Summary:  # type: ignore
    trxs = map(lambda line: Transaction.related_to(*line), lines)
    return sum(trxs, Summary())  # type: ignore


def get_account_aliased_by(file_path):  # type: ignore
    file_name = os.path.basename(file_path).split("_")[0]
    return core.Client.accounts().get(_params={"alias": file_name})[0]


def save_summary_related_to(account, summary):  # type: ignore
    summary_to_save = {
        "total_balance": summary.total_balance,
        "average_debit_amount": summary.average_debit_amount,
        "average_credit_amount": summary.average_credit_amount,
        "account": account["url"],
        "transactions": [],
    }
    summary_result = core.Client.summaries().post(summary_to_save)
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


def number_by_month(summary):  # type: ignore
    return {
        NAME_FOR[month]: amount
        for month, amount in summary.number_of_transactions_by_month.items()
    }


def replace_wildcards_in_email(  # type: ignore
    text,
    account,
    customer,
    summary,
):
    return text.format(
        account__identifier=account["identifier"],
        account__alias=account["alias"],
        customer__full_name=customer["full_name"],
        customer__chosen_name=customer["chosen_name"],
        customer__email=customer["email"],
        summary__total_balance=summary.total_balance,
        summary__average_debit_amount=summary.average_debit_amount,
        summary__average_credit_amount=summary.average_credit_amount,
        summary__transactions_per_month=number_by_month(summary),
    )


def send_email_by_gmail(account, summary):  # type: ignore
    mail_data = core.Client.mails_data().get(_params={"active": True})[0]
    customer = requests.get(account["customer"]).json()
    destination = customer["email"]
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(
        mail_data["sender"],
        str(os.environ.get("GMAIL_APP_PASSWORD")),
    )
    body = replace_wildcards_in_email(
        mail_data["body"],
        account,
        customer,
        summary,
    )
    email = MIMEText(body, "html")
    email["Subject"] = mail_data["subject"]
    email["From"] = mail_data["sender"]
    email["To"] = destination
    server.sendmail(mail_data["sender"], destination, email.as_string())


def process_file(file_path: str, task_id: str) -> None:
    with open(file_path, "r") as file:
        notify.success(task_id)  # File opened successfuly
        lines = csv.reader(file)
        next(lines, None)  # Ignore csv headers
        summary = get_summary_from(lines)
        account = get_account_aliased_by(file_path)
        save_summary_related_to(account, summary)
        notify.success(task_id)  # Summary saved in core.db
        send_email_by_gmail(account, summary)
        notify.success(task_id)  # Summary sent by email


@app.task(name="pendings")
def process(file_name: str, task_id: str) -> None:
    file_path = os.path.join(os.sep, "input", file_name)
    try:
        process_file(file_path, task_id)
    except (FileNotFoundError, KeyError):
        notify.error(task_id)
