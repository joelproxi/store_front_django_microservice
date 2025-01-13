

import json
import pika

from config import settings
from inventory.models import Inventory


class InventoryConsumer:
    def __init__(self):
        self.host = settings.RABBITMQ_HOST
        self.port = settings.RABBITMQ_PORT
        self.user = settings.RABBITMQ_USER
        self.password = settings.RABBITMQ_PASSWORD
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange="product_events",
            exchange_type="topic",
            durable=True,
        )
        self.channel.queue_declare("product_created", durable=True)
        self.channel.queue_bind(
            exchange="product_events",
            queue="product_created",
            routing_key="product.created",
        )
        
    def consume(self):
        self.channel.basic_consume(
            queue="product_created",
            on_message_callback=self._handle_product_created,
            auto_ack=True,
        )
        self.channel.start_consuming()
    
    def _handle_product_created(self, ch, method, properties, body):
        print("Product created event received")
        print(body)
        print("Product created event processed")
        print("")
        data = body
        try: 
            if isinstance(body, str):
                print("body is a string")
                data = json.loads(body)
            if isinstance(body, bytes):
                print("body is a bytes")
                data = json.loads(body.decode('utf-8'))
            print('Message recu: ', data)
            inventory, created = Inventory.objects.get_or_create(
                product_id=data["product_id"],
                price=data["price"],
                quantity=data.get("quantity", 0),
            )
            if created:
                print(f"Inventory record created: {inventory}")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
       
        except Exception as e:
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            print(e)