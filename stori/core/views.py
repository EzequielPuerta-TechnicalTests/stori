from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(["GET"])
def api_root(request, format=None):  # type: ignore
    return Response(
        {
            "customers_data": reverse(
                "customerdata-list",
                request=request,
                format=format,
            ),
            "accounts": reverse(
                "account-list",
                request=request,
                format=format,
            ),
            "mails_data": reverse(
                "maildata-list",
                request=request,
                format=format,
            ),
        }
    )
