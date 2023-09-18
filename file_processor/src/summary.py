from __future__ import annotations

from abc import ABC, abstractmethod

from src.months import MONTH


class Transaction(ABC):
    @classmethod
    def related_to(
        cls, provider_id: str, date: str, signed_amount: str
    ) -> "Transaction":
        symbol = signed_amount[0]
        if symbol == "+":
            return Credit(provider_id, date, signed_amount)
        elif symbol == "-":
            return Debit(provider_id, date, signed_amount)
        else:
            raise ValueError("Invalid transaction.")

    def __init__(self, provider_id: str, date: str, signed_amount: str):
        self.provider_id: str = provider_id
        self.date: str = date
        date_values = date.split("/")
        self.month: MONTH = int(date_values[0])
        self.day: int = int(date_values[1])
        self.amount: float = float(signed_amount[1:])

    def is_credit(self) -> bool:
        return False

    def is_debit(self) -> bool:
        return False

    @property
    @abstractmethod
    def signed_amount(self) -> float:
        pass

    def __repr__(self) -> str:
        return "{}<Id: {}, Date: {}, Amount: {}>".format(
            type(self).__name__,
            self.provider_id,
            self.date,
            self.signed_amount,
        )

    def __add__(
        self,
        other: int | float | Transaction | Summary,
    ) -> int | float | Summary:
        if isinstance(other, int) or isinstance(other, float):
            return round(other + self.signed_amount, 5)
        elif isinstance(other, Transaction):
            return Summary(of=[self, other])
        elif isinstance(other, Summary):
            return other + self
        else:
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    type(self), type(other)
                )
            )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Transaction)
            and self.is_credit() == other.is_credit()
            and self.provider_id == other.provider_id
            and self.date == other.date
            and self.signed_amount == other.signed_amount
        )

    def __hash__(self) -> int:
        return hash((self.provider_id, self.date, self.signed_amount))


class Credit(Transaction):
    def is_credit(self) -> bool:
        return True

    @property
    def signed_amount(self) -> float:
        return self.amount


class Debit(Transaction):
    def is_debit(self) -> bool:
        return True

    @property
    def signed_amount(self) -> float:
        return -self.amount


class Summary:
    def __init__(self, of: list[Transaction] = []):
        self.total_balance: float = 0
        self.average_debit_amount: float = 0
        self.average_credit_amount: float = 0
        self.number_of_transactions_by_month: dict[MONTH, int] = {}
        self.transactions_by_type: dict[type, list[Transaction]] = {
            Credit: [],
            Debit: [],
        }
        self.amounts_by_type: dict[type, list[float]] = {
            Credit: [],
            Debit: [],
        }

        for transaction in of:
            self + transaction

    @property
    def related_months(self) -> list[MONTH]:
        return list(self.number_of_transactions_by_month.keys())

    @property
    def transactions(self) -> list[Transaction]:
        credits = self.transactions_by_type[Credit]
        debits = self.transactions_by_type[Debit]
        return credits + debits

    def number_of_transactions_for(self, month: MONTH) -> int:
        try:
            return self.number_of_transactions_by_month[month]
        except KeyError:
            return 0

    def __repr__(self) -> str:
        return (
            f"Total balance: {self.total_balance}"
            + f" | Avg. Credit: {self.average_credit_amount}"
            + f" | Avg. Debit: {self.average_debit_amount}"
            + f" | # Trx by Month: {self.number_of_transactions_by_month}"
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Summary)
            and self.total_balance == other.total_balance
            and self.average_credit_amount == other.average_credit_amount
            and self.average_debit_amount == other.average_debit_amount
            and (
                self.number_of_transactions_by_month
                == other.number_of_transactions_by_month
            )
            and self.transactions_by_type == other.transactions_by_type
            and self.amounts_by_type == other.amounts_by_type
        )

    def __hash__(self) -> int:
        return hash((self.transactions_by_type,))

    def __add__(self, other: Transaction | Summary) -> Summary:
        if isinstance(other, Transaction):
            self.total_balance = other + self.total_balance  # type: ignore
            self.__register(other)
            self.average_credit_amount = self.__average_with(other, Credit)
            self.average_debit_amount = self.__average_with(other, Debit)
            return self
        elif isinstance(other, Summary):
            return sum(other.transactions, self)  # type: ignore
        else:
            raise TypeError(
                "unsupported operand type(s) for +: '{}' and '{}'".format(
                    type(self),
                    type(other),
                )
            )

    def __register(self, transaction: Transaction) -> None:
        try:
            self.number_of_transactions_by_month[transaction.month] += 1
        except KeyError:
            self.number_of_transactions_by_month[transaction.month] = 1
        kind = type(transaction)
        self.transactions_by_type[kind].append(transaction)
        self.amounts_by_type[kind].append(transaction.signed_amount)

    def __average_with(self, transaction: Transaction, kind: type) -> float:
        amounts = self.amounts_by_type[kind]
        try:
            return sum(amounts) / len(amounts)
        except ZeroDivisionError:
            return 0
