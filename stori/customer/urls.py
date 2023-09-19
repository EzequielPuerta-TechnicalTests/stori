from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path(
        "customer/data/",
        views.CustomerDataList.as_view(),
        name="customerdata-list",
    ),
    path(
        "customer/data/<int:pk>/",
        views.CustomerDataDetail.as_view(),
        name="customerdata-detail",
    ),
    path(
        "customer/accounts/",
        views.AccountList.as_view(),
        name="account-list",
    ),
    path(
        "customer/accounts/<int:pk>/",
        views.AccountDetail.as_view(),
        name="account-detail",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
