import pytest

from ..models import MailData
from ..serializers import MailDataSerializer


@pytest.mark.django_db
def test_mail_data_serializer() -> None:
    mail_data = MailData.objects.create(
        description="Automatic emails",
        sender="balances@stori.com",
        subject="Account balance",
        active=True,
        body="Hello, this is your balance summary.",
    )
    serializer = MailDataSerializer(
        instance=mail_data,
        context={"request": None},
    )

    _id = mail_data.id
    assert serializer.data["id"] == mail_data.id
    assert serializer.data["url"] == f"/mailing/mails_data/{_id}/"
    assert serializer.data["description"] == mail_data.description
    assert serializer.data["sender"] == mail_data.sender
    assert serializer.data["subject"] == mail_data.subject
    assert serializer.data["active"] == mail_data.active
    assert serializer.data["body"] == mail_data.body
    assert serializer.data["html_body"] == f"/mailing/mails_data/{_id}/body/"


@pytest.mark.django_db
def test_mail_data_serializer_for_empty_collection() -> None:
    queryset = MailData.objects.all()
    serializer = MailDataSerializer(
        queryset,
        many=True,
        context={"request": None},
    )
    assert serializer.data == []


@pytest.mark.django_db
def test_mail_data_serializer_for_all(persisted_mail_data) -> None:
    queryset = MailData.objects.all()
    serializer = MailDataSerializer(
        queryset,
        many=True,
        context={"request": None},
    )
    assert len(serializer.data) == 1
    mail_data = serializer.data[0]
    _id = mail_data["id"]
    assert mail_data["id"] == persisted_mail_data.id
    assert mail_data["url"] == f"/mailing/mails_data/{_id}/"
    assert mail_data["description"] == persisted_mail_data.description
    assert mail_data["sender"] == persisted_mail_data.sender
    assert mail_data["subject"] == persisted_mail_data.subject
    assert mail_data["active"] == persisted_mail_data.active
    assert mail_data["body"] == persisted_mail_data.body
    assert mail_data["html_body"] == f"/mailing/mails_data/{_id}/body/"
