# Generated by Django 4.2.5 on 2023-09-14 21:45

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MailData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "sender",
                    models.EmailField(
                        help_text="no-reply.balances@stori.com", max_length=100
                    ),
                ),
                (
                    "subject",
                    models.CharField(
                        help_text="Account Balance Update", max_length=100
                    ),
                ),
                ("active", models.BooleanField()),
                ("body", ckeditor.fields.RichTextField(blank=True, null=True)),
            ],
            options={
                "ordering": ["subject", "sender", "active"],
            },
        ),
    ]