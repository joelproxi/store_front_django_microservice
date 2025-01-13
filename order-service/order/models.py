from django.db import models


class Order(models.Model):
    first_name = models.CharField(
        max_length=50,
        null=True, blank=True)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    telephone = models.CharField(max_length=50)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='items')
    product_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} {self.quantity} {self.unit_price}"