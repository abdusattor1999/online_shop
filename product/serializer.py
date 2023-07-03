from rest_framework import serializers

from seller.models import Seller
from .models import Product, UploadImageProduct, Category, Attribute, AttributeValue


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


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer()

    class Meta:
        model = AttributeValue
        fields = ('id', 'attribute', 'value', 'status')


class ProductSerializer(serializers.ModelSerializer):
    # attributes = AttributeValueSerializer(many=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    seller = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all())

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'seller', 'description', 'price', 'discount', 'status', 'view')

    def create(self, validated_data):
        images = validated_data.pop('images', False)
        attributes = validated_data.pop("attributes", False)
        product = Product.objects.create(**validated_data)
        print('bu attributes 46 ;', attributes)
        if attributes:
            print("Buyer serializer 50: ", attributes)
            product.set_attributes(attributes)

        if images:
            product.set_images(images)
        return product

    def update(self, instance, validated_data):
        attributes = validated_data.pop('attributes', None)
        # instance = super().update(instance, validated_data)

        if attributes is not None:
            print("nested works")
            attribute_serializer = AttributeValueSerializer(instance.attributes, data=attributes)
            print(attribute_serializer)
            if attribute_serializer.is_valid():
                print("validated !!!")
                attribute_serializer.save()
                print(attribute_serializer)

        return instance
        return {"success": True, "message": "Product informations have been updated"}

    # def to_representation(self, instance):
    #     represent = super(ProductSerializer, self).to_representation(instance)
    #     represent['attribute'] = AttributeValueSer(instance.attributes.all(), many=True).data
    #     return represent
