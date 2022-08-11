import json

from django.conf import settings
from django.core.management import BaseCommand

from bills.models import ServiceClass


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(settings.BASE_DIR / 'serviceClass.json', 'r') as f:
            service_class_data = json.load(f)

        # to prevent creating records with existing code value
        existing_service_classes = ServiceClass.objects.values_list(
            'code', flat=True
        )
        service_class_data = [
            service for service in service_class_data
            if service['code'] not in existing_service_classes
        ]

        if service_class_data:
            services_to_create = [
                ServiceClass(**service) for service in service_class_data
            ]
            ServiceClass.objects.bulk_create(
                services_to_create,
                batch_size=len(services_to_create)
            )
            #  todo: logging hwo many created
