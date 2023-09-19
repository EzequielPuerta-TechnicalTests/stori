from rest_framework import generics, renderers
from rest_framework.response import Response

from .models import MailData
from .serializers import MailDataSerializer


class MailDataList(generics.ListCreateAPIView):
    queryset = MailData.objects.all()
    serializer_class = MailDataSerializer


class MailDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MailData.objects.all()
    serializer_class = MailDataSerializer


class MailDataBody(generics.GenericAPIView):
    queryset = MailData.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):  # type: ignore
        mail_data = self.get_object()
        return Response(mail_data.body)
