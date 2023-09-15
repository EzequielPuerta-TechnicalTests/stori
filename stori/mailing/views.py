from ckeditor.fields import RichTextFormField
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import MailData


class MailDataForm(ModelForm):
    class Meta:
        model = MailData
        fields = ["body"]
        widgets = {"body": RichTextFormField(config_name="default")}


def mails_data(request: HttpRequest) -> HttpResponse:
    num_mails_data = MailData.objects.all().count()
    return render(
        request,
        "mails_data.html",
        context={
            "num_mails_data": num_mails_data,
            "rich_text_form": MailDataForm(),
        },
    )
