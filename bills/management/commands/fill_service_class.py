import json
import logging

from django.conf import settings
from django.core.management import BaseCommand

from bills.models import ServiceClass


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Started filling ServiceClass based on json...")

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
            logger.info(
                f"Add {len(services_to_create)} new records to ServiceClass"
            )
        logger.info("Finished filling ServiceClass")
