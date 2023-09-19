import pytest

from ..models import MailData


def test_mail_data_attributes(mail_data) -> None:
    mail_data = mail_data()
    assert mail_data.description == "Automatic emails"
    assert mail_data.sender == "balances@stori.com"
    assert mail_data.subject == "Account balance"
    assert mail_data.active
    assert mail_data.body == "Hello, this is your balance summary."


def test_meta_ordering() -> None:
    assert MailData._meta.ordering == (
        "description",
        "subject",
        "sender",
        "active",
    )


def test_mail_data_representation(mail_data) -> None:
    mail_data = mail_data()
    assert str(mail_data) == "Account balance <Active: True>"


@pytest.mark.django_db
def test_mail_data_successful_creation() -> None:
    assert MailData.objects.count() == 0
    MailData.objects.create(
        description="Automatic emails",
        sender="balances@stori.com",
        subject="Account balance",
        active=True,
        body="Hello, this is your balance summary.",
    )
    assert MailData.objects.count() == 1
