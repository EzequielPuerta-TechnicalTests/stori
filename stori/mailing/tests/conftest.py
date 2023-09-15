from typing import Callable

import pytest

from ..models import MailData


@pytest.fixture
def mail_data() -> Callable[[], MailData]:
    def _mail_data() -> MailData:
        return MailData(
            description="Automatic emails",
            sender="balances@stori.com",
            subject="Account balance",
            active=True,
            body="Hello, this is your balance summary.",
        )

    yield _mail_data
