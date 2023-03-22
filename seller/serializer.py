from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Seller
from account.models import UploadFile


class CreateSellerSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    surname = serializers.CharField(required=True)
    shop_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    inn = serializers.CharField(max_length=10, required=True)
    bank_mfo = serializers.CharField(max_length=8,required=True)
    bank_account = serializers.CharField(required=True)
    shop_picture = serializers.ListField(required=False)
    bio = serializers.CharField(required=False)
    address = serializers.CharField(required=True)

    class Meta:
        model = Seller


class SellerEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ("first_name", "last_name", "surname", "shop_name", "email", "inn", "bank_mfo", "bank_account", "bio", "address")
        

        






    









