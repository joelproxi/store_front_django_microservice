from django.db import models


class Inventory(models.Model):
    product_id = models.IntegerField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    
    def __str__(self):
        return f"{self.product_id} - {self.quantity} - {self.price}"
