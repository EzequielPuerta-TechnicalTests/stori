from django.urls import path

from . import views

urlpatterns = [
    path("mails_data", views.mails_data, name="mails_data"),
]
