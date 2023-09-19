import pytest
from django.db.utils import DataError

from ..models import Account, CustomerData


def test_customer_data_attributes(customer_data) -> None:
    assert customer_data.full_name == "Ezequiel Puerta"
    assert customer_data.chosen_name == "Eze"
    assert customer_data.email == "ezepuerta@gmail.com"


def test_account_attributes(account, customer_data) -> None:
    assert account.customer == customer_data
    assert account.identifier == "111222333444555"
    assert account.alias == "ezequiel.puerta.ars"


def test_customer_data_meta_ordering() -> None:
    assert CustomerData._meta.ordering == ("full_name", "chosen_name", "email")


def test_account_meta_ordering() -> None:
    assert Account._meta.ordering == ("alias", "identifier")


def test_customer_data_representation(customer_data) -> None:
    assert str(customer_data) == "Ezequiel Puerta <ezepuerta@gmail.com>"


def test_account_representation(account) -> None:
    assert str(account) == "111222333444555 : ezequiel.puerta.ars"


@pytest.mark.django_db
def test_customer_data_name_validation() -> None:
    with pytest.raises(DataError) as exception:
        CustomerData.objects.create(
            full_name="Ezequiel Puerta" * 10,
            chosen_name="Eze",
            email="ezepuerta@gmail.com",
        )
    expected_error = "value too long for type character varying(100)\n"
    assert str(exception.value) == expected_error


@pytest.mark.django_db
def test_account_identifier_validation(persisted_customer_data) -> None:
    with pytest.raises(DataError) as exception:
        Account.objects.create(
            customer=persisted_customer_data,
            identifier="0123456789" * 4,
            alias="my.alias.mp",
        )
    expected_error = "value too long for type character varying(30)\n"
    assert str(exception.value) == expected_error


@pytest.mark.django_db
def test_customer_data_successful_creation() -> None:
    assert CustomerData.objects.count() == 0
    CustomerData.objects.create(
        full_name="Ezequiel Puerta",
        chosen_name="Eze",
        email="ezepuerta@gmail.com",
    )
    assert CustomerData.objects.count() == 1


@pytest.mark.django_db
def test_account_successful_creation(persisted_customer_data) -> None:
    assert Account.objects.count() == 0
    Account.objects.create(
        customer=persisted_customer_data,
        identifier="0123456789",
        alias="my.alias.mp",
    )
    assert Account.objects.count() == 1
