from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Warehouse, Product
from .serializers import WarehouseSerializer, ProductSerializer
from users.models import User

class WarehouseCreateView(generics.CreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

class SupplyProductView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        warehouse_id = request.data.get('warehouse_id')
        warehouse = Warehouse.objects.get(id=warehouse_id)

        if request.user.user_type != User.SUPPLIER:
            return Response({"detail": "Only suppliers can supply products."}, status=status.HTTP_403_FORBIDDEN)

        product.warehouse = warehouse
        product.save()
        return Response(self.get_serializer(product).data)

class RetrieveProductView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user.user_type != User.CONSUMER:
            return Response({"detail": "Only consumers can retrieve products."}, status=status.HTTP_403_FORBIDDEN)

        if product.quantity <= 0:
            return Response({"detail": "Not enough product in stock."}, status=status.HTTP_400_BAD_REQUEST)

        product.quantity -= 1
        product.save()
        return Response(self.get_serializer(product).data)