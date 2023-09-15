from django.db.models import CharField, EmailField, Model
from django.urls import reverse


class Account(Model):
    customer_name = CharField(max_length=100, help_text="John Doe")
    email = EmailField(max_length=256, help_text="john.doe@gmail.com")

    def __str__(self) -> str:
        return f"{self.customer_name} <{self.email}>"

    def get_absolute_url(self) -> str:
        return reverse("model-detail-view", args=[str(self.id)])

    class Meta:
        ordering = ("customer_name", "email")
