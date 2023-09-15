from ..admin import MailDataAdmin


def test_meta_list_display():
    assert MailDataAdmin.list_display == (
        "id",
        "description",
        "sender",
        "subject",
        "active",
    )
