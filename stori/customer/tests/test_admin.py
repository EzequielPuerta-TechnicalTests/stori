from ..admin import AccountAdmin


def test_meta_list_display() -> None:
    assert AccountAdmin.list_display == ("id", "customer_name", "email")
