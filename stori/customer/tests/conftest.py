from typing import Callable

import pytest

from ..models import Account


@pytest.fixture
def account() -> Callable[[str], Account]:
    def _account(customer_name: str = "Ezequiel Puerta") -> Account:
        email = "eze19.2009@gmail.com"
        return Account(customer_name=customer_name, email=email)

    yield _account
