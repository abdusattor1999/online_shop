from .models import Product, UploadImageProduct, Category, Attribute, AttributeValue
from rest_framework import serializers, status
from rest_framework.response import Response


class UploadImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImageProduct
        fields = ("id", "image", 'url')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")

    def create(self, validated_data):
        return super().create(validated_data)


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('id', "name", "status")

class AttributeValueSer(serializers.ModelSerializer):
    attribute = AttributeSerializer
    class Meta:
        model = AttributeValue
        fields = ('__all__')

class ProductSerializer(serializers.ModelSerializer):    
    # attributes = AttributeValueSer(many=True)
    category = CategorySerializer    
    # images = UploadImageProductSerializer    # Xatolik berdi : "Invalid pk \"8\" - object does not exist."

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'seller', 'description', "price", 'discount', "status", "view")








        