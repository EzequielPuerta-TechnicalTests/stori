from ..admin import MailDataAdmin


def test_meta_list_display() -> None:
    assert MailDataAdmin.list_display == (
        "id",
        "description",
        "sender",
        "subject",
        "active",
    )
