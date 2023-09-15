# Generated by Django 4.2.5 on 2023-09-14 22:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailing", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="maildata",
            options={
                "ordering": ["subject", "sender", "active"],
                "verbose_name": "mail data",
                "verbose_name_plural": "mails data",
            },
        ),
        migrations.AddField(
            model_name="maildata",
            name="description",
            field=models.CharField(
                default="Automatic email",
                help_text="Fields for automatic emails of account balances",
                max_length=100,
            ),
            preserve_default=False,
        ),
    ]