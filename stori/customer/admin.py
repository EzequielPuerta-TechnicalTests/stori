from django.contrib.admin import ModelAdmin, register

from .models import Account


@register(Account)
class AccountAdmin(ModelAdmin):
    list_display = ("id", "customer_name", "email")
