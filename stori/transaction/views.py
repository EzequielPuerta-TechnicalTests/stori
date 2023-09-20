from rest_framework import generics, status
from rest_framework.response import Response

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

    def list(self, request):  # type: ignore
        queryset = self.get_queryset()
        serializer = self.serializer_class(
            queryset,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    def post(self, request, format=None):  # type: ignore
        data = request.data
        if isinstance(data, list):
            serializer = self.get_serializer(
                data=request.data,
                many=True,
            )
        else:
            serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
