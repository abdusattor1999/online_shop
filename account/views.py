from django.shortcuts import render

# Create your views here.
from rest_framework.exceptions import ValidationError
from .serializers import (
    SignupSerializer, LogoutSerializer, 
    UploadImageSerializer, CreateProfileSerializer,  ProfilePicSerializer
    )
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, CreateAPIView
from .models import User, Profile, Cofirmation, Address, ProfilePictures, UploadFile
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import UploadFile, ProfilePictures



####################   USER MODEL  ################################## 

class SignupView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def validate_phone_number(self, phone):
        pattern = re.compile(r"^[\+]?[(]?[9]{2}?[8]{1}[)]?[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{7}$")
        if not pattern.match(phone):
            data = {
                "success":False,
                "message":"Telefon raqami to'g'ri kiritilmadi."
            }
            raise ValidationError(data)
        print('Validatsiya Muvaffaqiyatli !')
        return True


    def post(self, request, *args, **kwargs):
        phone = self.request.data.get('phone', None)
        self.validate_phone_number(phone=phone)
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'success':True,
            'message':"Arizangiz qabul qilindi. Kodni tasdiqlang !!!"
        }
        return Response(data)
    


class VerifyView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        code = self.request.data.get('code', None)
        data = request.data

        qs = Cofirmation.objects.filter(user__phone=data['phone'])

        if qs.exists():
            obj = qs.last()
            if obj.code != code:
                data = {
                    "success":False,
                    "message":"Noto'g'ri kod kiritildi"
                }
                return Response(data)
            obj.activate()
            
            return Response({"success": True, "message":"Kod tasdiqlandi. Ro'yxatdan o'tish muvaffaqiyatli"})
        else:
            return Response({"success": False, "message":"Telefon raqami xato"}, status=status.HTTP_404_NOT_FOUND)


class LoguotView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"success":True, "message":"Tizimdan chiqish muvaffaqiyatli !"}, status=status.HTTP_204_NO_CONTENT)
    

####################   USER MODEL  ################################## 


# 1 - Rasmni Fayl holatida yuklab serverga saqlaymiz va obyektni qaytaramiz
class UploadImageApiView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadImageSerializer


    def post(self, request, *args, **kwargs):
        try:
            file = UploadFile.objects.create(file=request.data['file'])
            return Response({"success": True, "message": "OK", "results": {"id": file.id, "url": file.url}})
        except Exception as e:
            return Response({"success": False, "message": str(e.args)}, status=status.HTTP_400_BAD_REQUEST)


# 2 - ProfilePictures modelida obyekt hosil qilib obyektni qaytaramiz 
# class ProfilePicView(APIView):
#     serializer_class = ProfilePicSerializer
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             user = self.request.get['user']
#             user = user
            
#             data = {
#                 "success":True,
#                 "message":"Rasm saqlandi",
#                 "results":image
#             }
#             return Response(data)
#         else:
#             return Response({"success":False, "message":"Rasm yuklash bajarilmadi"})



class CreateProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = self.request.user
        photo = serializer.data.get('photo', None)
        first_name = serializer.data.get('first_name', None)
        last_name = serializer.data.get('last_name', None)
        email = serializer.data.get("email", None)
        
        if photo is not None:
            image = UploadFile.objects.filter(id=photo)
            if image:
                ProfilePictures.objects.create(
                    instance_id = self.profile.profile_picture,
                    image_id = image.id
                )
            else:
                return Response(
                    {"success":False,"message":"Rasm yuklanmagan"}
                )

        user_exists = Profile.objects.filter(user=user).exists()
        
        if user_exists:
            raise ValueError({"success":False, "message":"Bu foydalanuvchi profili mavjud !"})
        else:
            user = Profile.objects.create(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.set_photo(photo)       

        data = {
            'success':True,
            'message':"Profil malumotlari saqlandi",
            "data":user
        }
        return Response(data)




class UpdateProfileView(UpdateAPIView):
    serializer_class = CreateProfileSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()

# --------------------------------------------------------------    


    








