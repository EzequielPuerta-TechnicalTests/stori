from rest_framework import serializers

from .models import Account, CustomerData


class CustomerDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomerData
        fields = (
            "id",
            "url",
            "full_name",
            "chosen_name",
            "email",
            "accounts",
        )


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "url",
            "customer",
            "identifier",
            "alias",
        )
