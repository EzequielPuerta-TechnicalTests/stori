import pytest

from ..models import Account, CustomerData
from ..serializers import AccountSerializer, CustomerDataSerializer


@pytest.mark.django_db
def test_customer_data_serializer_for_instance() -> None:
    customer_data = CustomerData.objects.create(
        full_name="Ezequiel Puerta",
        chosen_name="Eze",
        email="ezepuerta@gmail.com",
    )
    serializer = CustomerDataSerializer(
        instance=customer_data,
        context={"request": None},
    )

    _id = customer_data.id
    assert serializer.data["id"] == customer_data.id
    assert serializer.data["url"] == f"/customer/data/{_id}/"
    assert serializer.data["full_name"] == customer_data.full_name
    assert serializer.data["chosen_name"] == customer_data.chosen_name
    assert serializer.data["email"] == customer_data.email
    assert serializer.data["accounts"] == []


@pytest.mark.django_db
def test_account_serializer_for_instance(persisted_customer_data) -> None:
    assert (
        CustomerDataSerializer(
            instance=persisted_customer_data,
            context={"request": None},
        ).data["accounts"]
    ) == []

    account = Account.objects.create(
        customer=persisted_customer_data,
        identifier="0123456789",
        alias="my.alias.mp",
    )
    serializer = AccountSerializer(
        instance=account,
        context={"request": None},
    )

    _id = persisted_customer_data.id
    assert serializer.data["id"] == account.id
    assert serializer.data["url"] == f"/customer/accounts/{account.id}/"
    assert serializer.data["customer"] == f"/customer/data/{_id}/"
    assert serializer.data["identifier"] == account.identifier
    assert serializer.data["alias"] == account.alias

    assert (
        CustomerDataSerializer(
            instance=persisted_customer_data,
            context={"request": None},
        ).data["accounts"]
    ) == [serializer.data["url"]]


@pytest.mark.django_db
def test_customer_data_serializer_for_empty_collection() -> None:
    queryset = CustomerData.objects.all()
    serializer = CustomerDataSerializer(
        queryset,
        many=True,
        context={"request": None},
    )
    assert serializer.data == []


@pytest.mark.django_db
def test_account_serializer_for_empty_collection() -> None:
    queryset = Account.objects.all()
    serializer = AccountSerializer(
        queryset,
        many=True,
        context={"request": None},
    )
    assert serializer.data == []


@pytest.mark.django_db
def test_customer_data_serializer_for_all(persisted_customer_data) -> None:
    queryset = CustomerData.objects.all()
    serializer = CustomerDataSerializer(
        queryset,
        many=True,
        context={"request": None},
    )
    assert len(serializer.data) == 1
    customer_data = serializer.data[0]
    assert customer_data["id"] == persisted_customer_data.id
    assert customer_data["url"] == f"/customer/data/{customer_data['id']}/"
    assert customer_data["full_name"] == persisted_customer_data.full_name
    assert customer_data["chosen_name"] == persisted_customer_data.chosen_name
    assert customer_data["email"] == persisted_customer_data.email
    assert customer_data["accounts"] == []


@pytest.mark.django_db
def test_account_serializer_for_all(
    persisted_account,
    persisted_customer_data,
) -> None:
    queryset = Account.objects.all()
    serializer = AccountSerializer(
        queryset,
        many=True,
        context={"request": None},
    )
    assert len(serializer.data) == 1
    account = serializer.data[0]
    _id = persisted_customer_data.id
    assert account["id"] == persisted_account.id
    assert account["url"] == f"/customer/accounts/{account['id']}/"
    assert account["customer"] == f"/customer/data/{_id}/"
    assert account["identifier"] == persisted_account.identifier
    assert account["alias"] == persisted_account.alias
