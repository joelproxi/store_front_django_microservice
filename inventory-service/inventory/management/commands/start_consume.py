
from django.core.management.base import BaseCommand
from inventory.consumers import InventoryConsumer


class Command(BaseCommand):
    help = 'Consume messages from RabbitMQ'

    def handle(self, *args, **options):
        consumer = InventoryConsumer()
        consumer.consume()