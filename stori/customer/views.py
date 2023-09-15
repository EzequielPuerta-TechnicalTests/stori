from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import Account


def accounts(request: HttpRequest) -> HttpResponse:
    num_accounts = Account.objects.all().count()

    return render(
        request, "accounts.html", context={"num_accounts": num_accounts}
    )
