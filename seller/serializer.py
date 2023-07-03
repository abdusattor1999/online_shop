from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Seller
from account.models import UploadFile


class SellerEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = (
        "id", "first_name", "last_name", "surname", "shop_name", "email", "inn", "bank_mfo", "bank_account", "bio",
        "address")

    def validate(self, attrs):
        qs = Seller.objects.filter(email=attrs['email'])
        if qs.exists():
            return Response({"success": False, "message": "Bu Email oldin ro'yxatdan o'tgan boshqa pochta kiriting"})

        return super().validate(attrs)
