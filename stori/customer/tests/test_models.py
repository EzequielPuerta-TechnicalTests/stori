import pytest
from django.db.utils import DataError

from ..models import Account


def test_account_attributes(account) -> None:
    customer_account = account()
    assert customer_account.customer_name == "Ezequiel Puerta"
    assert customer_account.email == "eze19.2009@gmail.com"


def test_meta_ordering() -> None:
    assert Account._meta.ordering == ("customer_name", "email")


def test_account_representation(account) -> None:
    customer_account = account()
    assert str(customer_account) == "Ezequiel Puerta <eze19.2009@gmail.com>"


@pytest.mark.django_db
def test_account_customer_name_validation() -> None:
    name = "Ezequiel Puerta" * 10
    email = "eze19.2009@gmail.com"
    with pytest.raises(DataError) as exception:
        Account.objects.create(customer_name=name, email=email)
    expected_error = "value too long for type character varying(100)\n"
    assert str(exception.value) == expected_error


@pytest.mark.django_db
def test_account_successful_creation() -> None:
    assert Account.objects.count() == 0
    Account.objects.create(
        customer_name="Ezequiel Puerta", email="eze19.2009@gmail.com"
    )
    assert Account.objects.count() == 1
