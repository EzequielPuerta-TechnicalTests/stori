# Generated by Django 4.2.5 on 2023-09-15 17:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mailing", "0003_alter_maildata_options_alter_maildata_subject"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="maildata",
            options={
                "ordering": ("description", "subject", "sender", "active"),
                "verbose_name": "mail data",
                "verbose_name_plural": "mails data",
            },
        ),
    ]
