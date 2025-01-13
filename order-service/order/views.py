from rest_framework import viewsets

from order.models import Order
from order.serializers import OrderSerializer


class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer