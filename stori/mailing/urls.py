from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path(
        "mailing/mails_data/",
        views.MailDataList.as_view(),
        name="maildata-list",
    ),
    path(
        "mailing/mails_data/<int:pk>/",
        views.MailDataDetail.as_view(),
        name="maildata-detail",
    ),
    path(
        "mailing/mails_data/<int:pk>/body/",
        views.MailDataBody.as_view(),
        name="maildata-body",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
