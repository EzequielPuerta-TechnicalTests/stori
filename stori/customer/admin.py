from django.contrib.admin import ModelAdmin, register

from .models import Account, CustomerData


@register(CustomerData)
class CustomerDataAdmin(ModelAdmin):
    list_display = ("id", "full_name", "chosen_name", "email")


@register(Account)
class AccountAdmin(ModelAdmin):
    list_display = ("id", "customer", "identifier", "alias")
