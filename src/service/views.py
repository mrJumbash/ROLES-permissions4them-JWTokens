from rest_framework import generics
from rest_framework.response import Response
from service.serializers import ProductSerializer
from service.models import Product
from service.permissions import IsTenantAndAdminOrReadOnly, IsOwnerOrReadOnly

class ProductAPI(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsTenantAndAdminOrReadOnly]
    
    

class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset =  Product.objects.all()
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly] 
