from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from .models import Seller, ShopPictures
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializer import SellerEditSerializer
from account.models import UploadFile



class SellerEditView(RetrieveUpdateDestroyAPIView, ListAPIView):
    serializer_class = SellerEditSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Seller.objects.filter(user_id=user.id)
    
    def self_query_set(self, pk=None):
        spisok = []
        if pk is not None:
            seller = Seller.objects.filter(id=pk)
        else:
            seller = Seller.objects.all()
         
        if seller.exists():
            for sell in seller:
                spisok.append(
                    {
                        "id":sell.id,
                        "user_id":sell.user.id,
                        "first_name":sell.first_name,
                        "last_name":sell.last_name,
                        "surname":sell.surname,
                        "shop_name":sell.shop_name,
                        "inn":sell.inn,
                        "bank_mfo":sell.bank_mfo,
                        "bank_account":sell.bank_account,
                        "email":sell.email,
                        "bio":sell.bio,
                        "address":sell.address,
                        "shop_picture":sell.get_image()
                    }
                )
            return Response(spisok)
        else:
            return Response({"success":False, "message":"Bunday sotuvchi mavjud emas !"})


    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # -------- Fields ----------------------------------------
        user = self.request.user
        image = self.request.data.get('images', None)
        first_name = self.request.data.get('first_name', None)
        last_name = self.request.data.get('last_name', None)
        surname = self.request.data.get('surname', None)
        shop_name = self.request.data.get('shop_name', None)
        email = self.request.data.get('email', None)
        inn = self.request.data.get('inn', None)
        bank_mfo = self.request.data.get('bank_mfo', None)
        bank_account = self.request.data.get('bank_account', None)
        bio = self.request.data.get('bio', "")
        address = self.request.data.get("address", None)

        is_images = False

        def validate_picture(picture):
            qs = UploadFile.objects.filter(id=picture[0])
            if qs is None:
                raise Response({"success":False, "message":"Bunday rasm yuklanmagan"})
            else:  
                is_images=True
                return True
 
        user_exists = Seller.objects.filter(user=user).exists()
        
        if user_exists:
            return Response({"success":False, "message":"Bu userni sotuvchi profili mavjud !"})
        
        else:
            seller = Seller.objects.create(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                surname=surname,
                email=email,
                shop_name=shop_name,
                inn=inn,
                bank_mfo=bank_mfo,
                bank_account=bank_account,
                bio=bio,
                address=address
            )
            self.request.user.is_seller = True
            self.request.user.save()

        if image is not None:
            validate_picture(picture=image)
            seller.set_image(image)


        # if is_images:
        #         seller.set_image(images=image)

        data = {
            "success":True,
            "message":"Sotuvchi profili muvaffaqiyatli ochildi",
            "id":seller.id
            }
        return Response(data)



    def patch(self, request, *args, **kwargs):
        seller = Seller.objects.get(id=kwargs['pk'])
        images = request.data.pop("images", None)
        images = request.data.pop("images", None)
        if images is not None:
            seller.set_image(images)
        seller.update(request.data)
        return Response({"success":True, "message":"Do'kon malumotlari yangilandi"})

    def delete(self, request, *args, **kwargs):
        seller = Seller.objects.get(id=kwargs['pk'])
        seller.delete()     
        return Response({"success":True, "message":"Do'kon o'chirish muvaffaqiyatli"})

    def get(self, request, *args, **kwargs):
        return self.self_query_set(kwargs.get('pk', None))



