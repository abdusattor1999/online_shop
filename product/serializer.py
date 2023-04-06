from .models import Product, UploadImageProduct, Category
from rest_framework import serializers, status
from rest_framework.response import Response


class UploadImageProductSerializer(serializers.Serializer):
    class Meta:
        model = UploadImageProduct
        fields = ("image")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")

    def create(self, validated_data):
        return super().create(validated_data)


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    category = serializers.CharField(required=True)
    seller_id = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    discount = serializers.IntegerField(required=False)
    images = serializers.ListField(required=True)
    attributes = serializers.ListField(required=False)

    class Meta:
        model = Product













        