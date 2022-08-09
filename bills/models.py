from django.db import models


class BillInquiry(models.Model):
    client_name = models.CharField(max_length=50)
    client_org = models.CharField(max_length=100)
    number = models.PositiveIntegerField(help_text="Number of the bill")
    sum = models.DecimalField(max_digits=12, decimal_places=2,
                              help_text="Price of the service")
    date = models.DateField(help_text="Date when service has occurred")
    service = models.CharField(max_length=100, help_text="Service description")

    class Meta:
        ordering = ('client_name',)
