from rest_framework import generics

from .models import Summary, Transaction
from .serializers import SummarySerializer, TransactionSerializer


class SummaryList(generics.ListCreateAPIView):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer


class SummaryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Summary.objects.all()
    serializer_class = SummarySerializer


class TransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
