# Generated by Django 4.1 on 2022-08-11 11:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bills", "0003_billinquiry_service_class"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="billinquiry",
            unique_together={("client_name", "number")},
        ),
    ]