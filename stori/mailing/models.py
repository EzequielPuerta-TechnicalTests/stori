from ckeditor.fields import RichTextField
from django.db.models import BooleanField, CharField, EmailField, Model
from django.urls import reverse


class MailData(Model):
    description = CharField(
        max_length=100,
        help_text="Fields for automatic emails of account balances",
    )
    sender = EmailField(
        max_length=100, help_text="no-reply.balances@stori.com"
    )
    subject = CharField(max_length=100, help_text="Account Balance Summary")
    active = BooleanField()
    body = RichTextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.subject} <Active: {self.active}>"

    def get_absolute_url(self) -> str:
        return reverse("model-detail-view", args=[str(self.id)])

    class Meta:
        ordering = ("description", "subject", "sender", "active")
        verbose_name = "mail data"
        verbose_name_plural = "mails data"
