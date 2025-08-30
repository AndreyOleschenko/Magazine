from django.urls import path
from .views import WarehouseCreateView, ProductCreateView, SupplyProductView, RetrieveProductView

urlpatterns = [
    path('warehouses/', WarehouseCreateView.as_view(), name='warehouse-create'),
    path('products/', ProductCreateView.as_view(), name='product-create'),
    path('supply/', SupplyProductView.as_view(), name='supply-product'),
    path('retrieve/', RetrieveProductView.as_view(), name='retrieve-product'),
]