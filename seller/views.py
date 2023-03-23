from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, DestroyAPIView
from .models import Seller, ShopPictures
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializer import CreateSellerSerializer, SellerEditSerializer
from account.models import UploadFile


class CreateSellerView(ListCreateAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = CreateSellerSerializer
    
    def get_queryset(self):
        return Seller.objects.all()
    
    def post(self, request):
        serializer = self.serilizer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # -------- Fields ----------------------------------------
        image = self.request.data.get('shop_picture', None)
        user = self.request.user
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


        if image is not None:
            validate_picture(picture=image)
            is_images = True
            print("image is not none from views 83")
            seller.set_image(image)

        else:   
            return Response({"success":False,"message":"Bunday rasm yuklanmagan"})
        
        if is_images:
                print("is_image = True from views 90")
                seller.set_image(images=image)

        data = {
            "success":True,
            "message":"Sotuvchi profili muvaffaqiyatli ochildi"
            }
        return Response(data)




class SellerEditView(RetrieveUpdateDestroyAPIView):
    serializer_class = SellerEditSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Seller.objects.filter(user_id=user.id)
    
    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response({"success":True, "message":"Profil malumotlari yangilandi"})

    def delete(self, request, *args, **kwargs):     
        self.destroy(request, *args, **kwargs)
        return Response({"success":True, "message":"Do'kon o'chirish muvaffaqiyatli"})




