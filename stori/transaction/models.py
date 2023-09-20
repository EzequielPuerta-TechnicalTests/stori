from customer.models import Account
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Summary(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    total_balance = models.FloatField(help_text="999.99")
    average_debit_amount = models.FloatField(help_text="123.50")
    average_credit_amount = models.FloatField(help_text="123.50")
    account = models.ForeignKey(
        Account,
        related_name="summaries",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        msg = "<Total: {} | Avg Debit: {} | Avg Credit: {} | Account: {}>"
        return msg.format(
            self.total_balance,
            self.average_debit_amount,
            self.average_credit_amount,
            self.account,
        )

    class Meta:
        ordering = ("account", "-created")
        verbose_name = "summary"
        verbose_name_plural = "summaries"


class Transaction(models.Model):
    provider_id = models.CharField(max_length=50, help_text="123")
    day = models.IntegerField(
        help_text="1-31",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(31),
        ],
    )
    month = models.IntegerField(
        help_text="1-12",
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12),
        ],
    )
    amount = models.FloatField(help_text="123.45")
    summary = models.ForeignKey(
        Summary,
        related_name="transactions",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return "<{}, {}/{}, {}>".format(
            self.provider_id, self.month, self.day, self.amount
        )

    class Meta:
        ordering = ("-summary", "-month", "-day")
