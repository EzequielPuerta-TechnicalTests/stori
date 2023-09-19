from src.months import AUGUST, JULY, MONTH, YEAR
from src.summary import Credit, Debit, Summary, Transaction


def rest_of_the_year(current_months: list[MONTH]) -> list[MONTH]:
    return [month for month in YEAR if (month not in current_months)]


def test_credit_creation() -> None:
    data = ("0", "7/15", "+60.5")
    transaction = Transaction.related_to(*data)
    assert isinstance(transaction, Credit)
    assert transaction.is_credit()
    assert not transaction.is_debit()
    assert transaction.provider_id == "0"
    assert transaction.date == "7/15"
    assert transaction.month == 7
    assert transaction.day == 15
    assert transaction.amount == 60.5
    assert transaction.signed_amount == 60.5


def test_debit_creation() -> None:
    data = ("1", "7/28", "-10.3")
    transaction = Transaction.related_to(*data)
    assert isinstance(transaction, Debit)
    assert not transaction.is_credit()
    assert transaction.is_debit()
    assert transaction.provider_id == "1"
    assert transaction.date == "7/28"
    assert transaction.month == 7
    assert transaction.day == 28
    assert transaction.amount == 10.3
    assert transaction.signed_amount == -10.3


def test_credit_representation() -> None:
    data = ("0", "7/15", "+60.5")
    transaction = Transaction.related_to(*data)
    assert repr(transaction) == "Credit<Id: 0, Date: 7/15, Amount: 60.5>"


def test_debit_representation() -> None:
    data = ("1", "7/28", "-10.3")
    transaction = Transaction.related_to(*data)
    print(str(transaction))
    assert repr(transaction) == "Debit<Id: 1, Date: 7/28, Amount: -10.3>"


def test_transaction_equality() -> None:
    credit = Transaction.related_to("0", "7/15", "+60.5")
    same_credit = Transaction.related_to("0", "7/15", "+60.5")
    other_credit = Transaction.related_to("0", "7/15", "+60")
    debit = Transaction.related_to("1", "7/28", "-10.3")
    assert credit == same_credit
    assert not credit == other_credit
    assert not credit == debit


def test_transaction_hashing() -> None:
    credit = Transaction.related_to("0", "7/15", "+60.5")
    same_credit = Transaction.related_to("0", "7/15", "+60.5")
    other_credit = Transaction.related_to("0", "7/15", "+60")
    debit = Transaction.related_to("1", "7/28", "-10.3")
    assert set((credit,)) == set((same_credit,))
    assert not set((credit,)) == set((other_credit,))
    assert not set((credit,)) == set((debit,))


def test_credit_and_number_addition() -> None:
    transaction = Transaction.related_to("0", "7/15", "+60.5")
    assert transaction + 10 == 70.5
    assert transaction + 0.5 == 61
    assert transaction + -10 == 50.5
    assert transaction + -100.5 == -40


def test_debit_and_number_addition() -> None:
    transaction = Transaction.related_to("1", "7/28", "-10.3")
    assert transaction + 20 == 9.7
    assert transaction + 30.3 == 20
    assert transaction + 0.3 == -10
    assert transaction + -10 == -20.3


def test_summary_creation() -> None:
    summary = Summary()

    assert summary.total_balance == 0
    assert summary.related_months == []

    for month in YEAR:
        assert summary.number_of_transactions_for(month) == 0

    assert summary.transactions == []
    assert summary.average_debit_amount == 0
    assert summary.average_credit_amount == 0


def test_summary_initialization() -> None:
    transaction = Transaction.related_to("0", "7/15", "+60.5")
    summary = Summary(of=[transaction])

    assert summary.total_balance == transaction.signed_amount
    assert summary.related_months == [transaction.month]

    assert transaction.month == JULY
    for month in rest_of_the_year(summary.related_months):
        assert summary.number_of_transactions_for(month) == 0
    assert summary.number_of_transactions_for(JULY) == 1

    assert summary.transactions == [transaction]
    assert summary.average_debit_amount == 0
    assert summary.average_credit_amount == transaction.signed_amount


def test_credit_and_summary_addition() -> None:
    transaction = Transaction.related_to("0", "7/15", "+60.5")
    summary = Summary() + transaction

    assert summary.total_balance == transaction.signed_amount
    assert summary.related_months == [transaction.month]

    assert transaction.month == JULY
    for month in rest_of_the_year(summary.related_months):
        assert summary.number_of_transactions_for(month) == 0
    assert summary.number_of_transactions_for(JULY) == 1

    assert summary.transactions == [transaction]
    assert summary.average_debit_amount == 0
    assert summary.average_credit_amount == transaction.signed_amount


def test_debit_and_summary_addition() -> None:
    transaction = Transaction.related_to("1", "7/28", "-10.3")
    summary = Summary() + transaction

    assert summary.total_balance == transaction.signed_amount
    assert summary.related_months == [transaction.month]

    assert transaction.month == JULY
    for month in rest_of_the_year(summary.related_months):
        assert summary.number_of_transactions_for(month) == 0
    assert summary.number_of_transactions_for(JULY) == 1

    assert summary.transactions == [transaction]
    assert summary.average_debit_amount == transaction.signed_amount
    assert summary.average_credit_amount == 0


def test_merge_two_credits() -> None:
    first_credit = Transaction.related_to("0", "7/15", "+60.5")
    second_credit = Transaction.related_to("3", "8/13", "+10")
    summary = first_credit + second_credit
    assert isinstance(summary, Summary)
    assert summary.total_balance == 70.5
    assert summary.related_months == [7, 8]

    for month in rest_of_the_year(summary.related_months):
        assert summary.number_of_transactions_for(month) == 0
    assert summary.number_of_transactions_for(JULY) == 1
    assert summary.number_of_transactions_for(AUGUST) == 1

    assert len(summary.transactions) == 2
    assert first_credit in summary.transactions
    assert second_credit in summary.transactions
    assert summary.average_debit_amount == 0
    assert summary.average_credit_amount == 35.25


def test_merge_two_credits_iteratively() -> None:
    first_credit = Transaction.related_to("0", "7/15", "+60.5")
    summary = Summary() + first_credit
    second_credit = Transaction.related_to("3", "8/13", "+10")
    summary = summary + second_credit
    assert summary == first_credit + second_credit


def test_summary_initialization_with_multiple_transactions() -> None:
    first_credit = Transaction.related_to("0", "7/15", "+60.5")
    second_credit = Transaction.related_to("3", "8/13", "+10")
    summary = Summary(of=[first_credit, second_credit])
    assert summary == first_credit + second_credit


def test_merge_multiple_transactions() -> None:
    first = Transaction.related_to("0", "7/15", "+60.5")
    second = Transaction.related_to("1", "7/28", "-10.3")
    third = Transaction.related_to("2", "8/2", "-20.46")
    fourth = Transaction.related_to("3", "8/13", "+10")

    summary1 = ((first + second) + third) + fourth  # type: ignore
    summary2 = first + (second + (third + fourth))
    summary3 = (first + second) + (third + fourth)  # type: ignore
    summary4 = sum([second, third, fourth], first)
    summary5 = sum([first, second, third, fourth], Summary())

    assert not summary1 == summary2
    assert summary1 == summary3
    assert summary1 == summary4
    assert summary1 == summary5


def test_round_transaction_addition() -> None:
    amount1 = 60.5
    amount2 = -10.3
    amount3 = -20.46
    amount4 = 10
    result = amount1 + (amount2 + (amount3 + amount4))
    assert result == 39.739999999999995

    first = Transaction.related_to("0", "7/15", "+60.5")
    second = Transaction.related_to("1", "7/28", "-10.3")
    third = Transaction.related_to("2", "8/2", "-20.46")
    fourth = Transaction.related_to("3", "8/13", "+10")
    summary = first + (second + (third + fourth))
    assert summary.total_balance == 39.74  # type: ignore
