from rest_framework import serializers

from .models import Summary, Transaction


class SummarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Summary
        fields = (
            "id",
            "url",
            "created",
            "total_balance",
            "average_debit_amount",
            "average_credit_amount",
            "account",
            "transactions",
        )


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id",
            "url",
            "provider_id",
            "day",
            "month",
            "amount",
            "summary",
        )
