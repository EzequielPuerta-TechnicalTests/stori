from django.db.models import CASCADE, CharField, EmailField, ForeignKey, Model


class CustomerData(Model):
    full_name = CharField(max_length=100, help_text="John Doe")
    chosen_name = CharField(max_length=40, help_text="John")
    email = EmailField(max_length=256, help_text="john.doe@gmail.com")

    def __str__(self) -> str:
        return f"{self.full_name} <{self.email}>"

    class Meta:
        ordering = ("full_name", "chosen_name", "email")
        verbose_name = "customer data"
        verbose_name_plural = "customers data"


class Account(Model):
    customer = ForeignKey(
        CustomerData,
        related_name="accounts",
        on_delete=CASCADE,
    )
    identifier = CharField(max_length=30, help_text="123456789012345678901")
    alias = CharField(max_length=50, help_text="my.alias.account")

    def __str__(self) -> str:
        return f"{self.identifier} : {self.alias}"

    class Meta:
        ordering = ("alias", "identifier")
