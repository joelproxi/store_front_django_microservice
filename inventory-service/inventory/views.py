import logging
from decimal import Decimal

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from inventory.models import Inventory
from inventory.serializers import InventorySerializer


logger = logging.getLogger(__name__)


class InventoryListCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        inventory_data = request.data
        serializer = InventorySerializer(data=inventory_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        inventory_data = Inventory.objects.all()
        serializer = InventorySerializer(inventory_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
      
class InventoryRetreiveUpdateAPIView(APIView):
    def get(self, request, id, *args, **kwargs):
        inventory = get_object_or_404(Inventory, pk=id)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, id, *args, **kwargs):
        inventory_json = request.data
        inventory = get_object_or_404(Inventory, pk=id)
        quantity = inventory_json.get('quantity')
        if quantity is not None:
            inventory.quantity = (inventory.quantity) - Decimal(quantity)
            inventory.save()
            serializer = InventorySerializer(inventory)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Qauntity is required"}, status=status.HTTP_400_BAD_REQUEST)

