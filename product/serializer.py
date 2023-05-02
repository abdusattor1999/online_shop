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
    attributes = AttributeValueSer(many=True)
    category = CategorySerializer()    
    # images = UploadImageProductSerializer    # Xatolik berdi : "Invalid pk \"8\" - object does not exist."

    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'seller', 'description', "price", 'discount', "status", "view", "attributes",)


    def update(self, instance, validated_data):
        attributes = validated_data.pop("attributes", False)
        images = validated_data.pop("images", False)
        if attributes:
            for attr in attributes:
                print("Bu attr", dict(attr))
                print("Bu attr2", type(attr))

                # attribute_value = AttributeValue.objects.filter(id=attr['id']).last()
                # attribute_value = attr[0]
            #     status = attribute_value.status
            #     value = attribute_value.value
            #     attribute_value.status = attr[0].get('status', status)
            #     attribute_value.status = attr[0].get('value', value)
            # attribute_value.save()
        
        if images:
            instance.set_images(images)
        if len(validated_data) > 0:
            super().update(instance, validated_data)

        return {"success":True, "message":"Product informations have been updated"}






        