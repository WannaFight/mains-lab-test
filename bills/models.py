from django.core.validators import MinValueValidator
from django.db import models


class BillInquiry(models.Model):
    client_name = models.CharField(max_length=50)
    client_org = models.CharField(max_length=100)
    number = models.PositiveIntegerField(help_text="Number of the bill")
    sum = models.DecimalField(max_digits=12, decimal_places=2,
                              help_text="Price of the service")
    date = models.DateField(help_text="Date when service has occurred")
    service = models.CharField(max_length=100, help_text="Service description")
    service_class = models.ForeignKey('bills.ServiceClass', null=True,
                                      related_name='bill_inquiries',
                                      on_delete=models.SET_NULL)

    class Meta:
        ordering = ('client_name',)


class ServiceClass(models.Model):
    CONSULTATION = 'консультация'
    TREATMENT = 'лечение'
    HOSPITAL = 'стационар'
    DIAGNOSTICS = 'диагностика'
    LABORATORY = 'лаборатория'

    NAME_CHOICES = [
        (CONSULTATION, 'Консультация'),
        (TREATMENT, 'Лечение'),
        (HOSPITAL, 'Стационар'),
        (DIAGNOSTICS, 'Диагностика'),
        (LABORATORY, 'Лаборатория')
    ]

    name = models.CharField(choices=NAME_CHOICES, max_length=20)
    code = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)], unique=True,
        help_text="Unique code for service class"
    )

    def __str__(self) -> str:
        return f"{self.name}(code: {self.code})"
