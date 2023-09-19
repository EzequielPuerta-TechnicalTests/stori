from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path(
        "summaries/",
        views.SummaryList.as_view(),
        name="summary-list",
    ),
    path(
        "summaries/<int:pk>/",
        views.SummaryDetail.as_view(),
        name="summary-detail",
    ),
    path(
        "transactions/",
        views.TransactionList.as_view(),
        name="transaction-list",
    ),
    path(
        "transactions/<int:pk>/",
        views.TransactionDetail.as_view(),
        name="transaction-detail",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
