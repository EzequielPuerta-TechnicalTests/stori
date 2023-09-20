from rest_framework import generics

from .models import Account, CustomerData
from .serializers import AccountSerializer, CustomerDataSerializer


class CustomerDataList(generics.ListCreateAPIView):
    queryset = CustomerData.objects.all()
    serializer_class = CustomerDataSerializer


class CustomerDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerData.objects.all()
    serializer_class = CustomerDataSerializer


class AccountList(generics.ListCreateAPIView):
    # queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):  # type: ignore
        queryset = Account.objects.all()
        identifier = self.request.query_params.get("identifier")
        if identifier is not None:
            return queryset.filter(identifier=identifier)
        else:
            alias = self.request.query_params.get("alias")
            if alias is not None:
                return queryset.filter(alias=alias)
            else:
                return queryset


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
