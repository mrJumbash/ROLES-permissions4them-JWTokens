from rest_framework import serializers
from service.models import Product

class ProductSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255) 
    description = serializers.CharField(required=False)
    price = serializers.IntegerField(max_value=255)
    owmer = serializers.HiddenField(default=serializers.CurrentUserDefault)
    
    def create(self, validated_data):
        return Product.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance