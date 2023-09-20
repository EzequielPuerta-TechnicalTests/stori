from __future__ import annotations

import os

import requests  # type: ignore


class Client:
    def __init__(self, resource: str = "") -> None:
        self.base_url: str = "http://core:{}/{}".format(
            os.environ.get("INTERNAL_STORI_CORE_PORT"), resource
        )

    @classmethod
    def customers_data(cls) -> "Client":
        return cls("customer/data")

    @classmethod
    def accounts(cls) -> "Client":
        return cls("customer/accounts")

    @classmethod
    def mails_data(cls) -> "Client":
        return cls("mailing/mails_data")

    @classmethod
    def summaries(cls) -> "Client":
        return cls("summaries")

    @classmethod
    def transactions(cls) -> "Client":
        return cls("transactions")

    def get(
        self,
        _id: int | None = None,
        _params: dict | None = None,  # type: ignore
    ) -> requests.Response:
        if _id:
            url = f"{self.base_url}/{_id}/"
        else:
            if _params:
                params = [f"{key}={value}" for key, value in _params.items()]
                url = f"{self.base_url}?{'&'.join(params)}"
            else:
                url = f"{self.base_url}/"
        return requests.get(url)

    def post(self, data) -> requests.Response:  # type: ignore
        return requests.post(f"{self.base_url}/", json=data)
