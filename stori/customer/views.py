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
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
