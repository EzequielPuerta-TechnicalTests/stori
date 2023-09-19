from ..admin import AccountAdmin, CustomerDataAdmin


def test_customer_data_meta_list_display() -> None:
    expected = ("id", "full_name", "chosen_name", "email")
    assert CustomerDataAdmin.list_display == expected


def test_account_meta_list_display() -> None:
    expected = ("id", "customer", "identifier", "alias")
    assert AccountAdmin.list_display == expected
