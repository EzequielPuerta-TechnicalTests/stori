# Generated by Django 4.2.5 on 2023-09-14 22:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("mailing", "0002_alter_maildata_options_maildata_description"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="maildata",
            options={
                "ordering": ["description", "subject", "sender", "active"],
                "verbose_name": "mail data",
                "verbose_name_plural": "mails data",
            },
        ),
        migrations.AlterField(
            model_name="maildata",
            name="subject",
            field=models.CharField(
                help_text="Account Balance Summary", max_length=100
            ),
        ),
    ]
