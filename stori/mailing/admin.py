from django.contrib.admin import ModelAdmin, register

from .models import MailData


@register(MailData)
class MailDataAdmin(ModelAdmin):
    list_display = ("id", "description", "sender", "subject", "active")
