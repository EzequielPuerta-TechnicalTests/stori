import pytest

from ..models import Account, CustomerData


@pytest.fixture
def customer_data() -> CustomerData:
    yield CustomerData(
        full_name="Ezequiel Puerta",
        chosen_name="Eze",
        email="ezepuerta@gmail.com",
    )


@pytest.fixture
def persisted_customer_data() -> CustomerData:
    yield CustomerData.objects.create(
        full_name="Ezequiel Puerta",
        chosen_name="Eze",
        email="ezepuerta@gmail.com",
    )


@pytest.fixture
def account(customer_data) -> Account:
    yield Account(
        customer=customer_data,
        identifier="111222333444555",
        alias="ezequiel.puerta.ars",
    )


@pytest.fixture
def persisted_account(persisted_customer_data) -> Account:
    yield Account.objects.create(
        customer=persisted_customer_data,
        identifier="111222333444555",
        alias="ezequiel.puerta.ars",
    )
