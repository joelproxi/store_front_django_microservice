
import requests
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.transaction import atomic
from order.models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
        extra_kwargs = {
            "order": {"read_only": True},
        }


class OrderSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='telephone')
    order_items = OrderItemSerializer(many=True, source="items")

    class Meta:
        model = Order
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "order_items"
        ]


    @atomic()
    def create(self, validated_data):
        order_items_data = validated_data.pop("items")
        self._validated_inventory(order_items_data)
        order = Order.objects.create(
            **validated_data
        )
        self._create_order_items(order, order_items_data)
        return order

    def _validated_inventory(self, order_items_data):
        for order_item in order_items_data:
            # product = get_object_or_404(Product, id=order_item["product"].pk)
            # if order_item["quantity"] > product.stock:
            product_id = order_item.get('product_id')
            requested_quantity = order_item.get('quantity')
            resp = requests.get(f"http://127.0.0.1:9501/api/v1/inventories/{product_id}/")
            
            if resp.status_code == 200:
                inventory_data = resp.json()
                available_quantity = inventory_data.get('quantity')
                
                if available_quantity < requested_quantity:
                    raise serializers.ValidationError(f"Stock insuffissant pour le produit: {product_id}"
                                                  f"Quantite demandée est: {requested_quantity}, et disponible est: {available_quantity}")
            else:
                raise serializers.ValidationError("Service indispoible")
            
    def _create_order_items(self, order, order_items_data):
        for order_item in order_items_data:
            OrderItem.objects.create(
                order=order,
                product_id=order_item['product_id'],
                quantity=order_item["quantity"],
                unit_price=order_item["unit_price"]
            )
            self._update_inevntory_quantity({
                "product_id": order_item['product_id'],
                "quantity": order_item["quantity"],
            })
            
    def _update_inevntory_quantity(self, item):
        product_id = item["product_id"]
        new_quantity = item["quantity"]
        try:
            response = requests.put(f"http://127.0.0.1:9501/api/v1/inventories/{product_id}/",
                                    json={"quantity": new_quantity})
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError(e)
            

