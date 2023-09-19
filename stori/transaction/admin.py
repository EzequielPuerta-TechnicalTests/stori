from django.contrib.admin import ModelAdmin, register

from .models import Summary, Transaction


@register(Summary)
class SummaryAdmin(ModelAdmin):
    list_display = (
        "id",
        "created",
        "account",
        "total_balance",
        "average_debit_amount",
        "average_credit_amount",
    )


@register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = (
        "id",
        "provider_id",
        "amount",
        "day",
        "month",
        "summary",
    )
