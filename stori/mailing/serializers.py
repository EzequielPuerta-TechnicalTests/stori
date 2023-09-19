from ckeditor.fields import RichTextFormField
from rest_framework import serializers

from .models import MailData


class MailDataSerializer(serializers.HyperlinkedModelSerializer):
    html_body = serializers.HyperlinkedIdentityField(
        view_name="maildata-body", format="html"
    )

    class Meta:
        model = MailData
        fields = (
            "id",
            "url",
            "description",
            "sender",
            "subject",
            "active",
            "body",
            "html_body",
        )
        widgets = {"body": RichTextFormField(config_name="default")}
