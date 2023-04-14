from .utils import send_code
from rest_framework.exceptions import ValidationError
from .serializers import (
    AddressSerializer, SignupSerializer, LogoutSerializer, ChangePasswordSerializer,
    UploadImageSerializer, CreateProfileSerializer,  ProfilePicSerializer,
    ChangePhoneSerializer, DeleteUserSerilizer, LoginSerializer
    )
from random import randrange
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, CreateAPIView
from .models import User, Profile, Cofirmation, Address, ProfilePictures, UploadFile
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
import re
from .models import UploadFile, ProfilePictures

######################   UTIL   ############################################


def set_image_profile(profile, images:list, is_images=None):
    file = UploadFile.objects.filter(id=images[0])
    if file.exists():
        profile.set_image(images)
    else:
        return Response(
            {"success": False, "message": "Bunday rasm yuklanmagan"}
        )
    if is_images:
        profile.set_image(images=images)

####################   USER MODEL  ##################################

class SignupView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = SignupSerializer

    def validate_phone_number(self, phone):
        pattern = re.compile(
            r"^[\+]?[(]?[9]{2}?[8]{1}[)]?[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{7}$")
        if not pattern.match(phone):
            data = {
                "success": False,
                "message": "Telefon raqami to'g'ri kiritilmadi."
            }
            raise ValidationError(data)
        print('Validatsiya Muvaffaqiyatli !')
        return True

    def post(self, request, *args, **kwargs):
        phone = self.request.data.get('phone', None)
        self.validate_phone_number(phone=phone)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'success': True,
            'message': "Ro'yxatdan o'tish uchun arizangiz qabul qilindi. Kodni tasdiqlang !!!"
        }
        return Response(data)


class VerifyView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        phone = self.request.data.get("phone", None)
        new_phone = self.request.data.get("new_phone", None)
        code = self.request.data.get('code', None)
        type = self.request.data.get("type", None)
        lists = [phone, new_phone, code, type]
        if None in lists and type == "change_phone":
            return Response({"success": False, "message": f"Hamma malumotlar berilmadi \nKerakli malumotlar:{lists}"})
        qs = Cofirmation.objects.filter(
            user__phone=phone, expiration_time__gte=timezone.now())
        obj = qs.last()

        # kod muddati tugamagan obyekt bor bo'lsa
        if qs.exists():
            if obj.code != str(code):
                data = {
                    "success": False,
                    "message": "Noto'g'ri kod kiritildi"
                }
                return Response(data)
            obj.activate()

            if type == "change_phone":
                user = User.objects.filter(phone=phone).last()
                user.phone = new_phone
                user.is_active = True
                user.save()

                text = "Kod tasdiqlandi. Telefon raqamni yangilash muvaffaqiyatli"
            elif type == "password_reset":
                text = "Kod tasdiqlandi. Parol tiklashga ruxsat berildi"
            else:  # resend and register
                text = "Kod tasdiqlandi. Ro'yxatdan o'tish muvaffaqiyatli"

            return Response({"success": True, "message": text})
        else:
            if Cofirmation.objects.filter(user__phone=self.request.data['phone']):
                response = {
                    "success": False, "message": "Kod muddati o'tgan davom etish uchun kodni qayta yuboring"}
                return Response(response)
            else:
                response = {"success": False, "message": "Telefon raqami xato"}
                return Response(response, status=status.HTTP_404_NOT_FOUND)

#--------------------------------------------------------------
from rest_framework_simplejwt.views import TokenViewBase

class LoginView(TokenViewBase):
    serializer_class = LoginSerializer


class LoguotView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"success": True, "message": "Tizimdan chiqish muvaffaqiyatli !"}, status=status.HTTP_204_NO_CONTENT)


class ChangePhoneView(APIView):
    permission_classes = (IsAuthenticated,)

    def validate_phone_number(self, phone):
        pattern = re.compile(
            r"^[\+]?[(]?[9]{2}?[8]{1}[)]?[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{7}$")
        if not pattern.match(phone):
            data = {
                "success": False,
                "message": "Yangi telefon raqami to'g'ri kiritilmadi."
            }
            raise ValidationError(data)
        print('Validatsiya Muvaffaqiyatli !')
        return True

    def patch(self, request):
        serializer = ChangePhoneSerializer(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            phone = serializer.validated_data['new_phone']
            self.validate_phone_number(phone)
            user.edit_phone()
            return Response({"success": True, 'message': "Telefon Raqam yangiash so'rovi yuborildi kodni tasdiqlang !"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        self.object = self.request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"success": False, "message": "Parol noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'success': True,
                'message': 'Parol yangilash muvaffaqiyatli bajarildi',
                'status': status.HTTP_200_OK,
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = DeleteUserSerilizer
    permission_classes = IsAuthenticated,

    def get_user_data(self, pk=False):
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        user_list = []
        for user in users:
            data = {
                "id" : user.id,
                "phone" : user.phone ,
                "is_seller" : user.is_seller ,
                "is_active" : user.is_active
            }

            profile = Profile.objects.filter(user=user)
            if profile.exists():
                pr = profile.last()
                data['profile'] = pr.id

            if user.is_seller==True:
                data['seller'] = user.seller.id

            user_list.append(data)
            
        if pk:
            return Response(user_list[0])
        else:    
            return Response(user_list)
    
    def get(self, request, *args, **kwargs):
        return self.get_user_data(kwargs.get("pk", False))


    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({"success": True, "message": "Foydalanuvchi hisobi o'chirildi"})


class ResetPassRequestView(APIView):
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        phone = self.request.data.get('phone', None)
        qs = User.objects.filter(phone=phone)
        user = qs.last()
        if qs.exists():
            code = "".join(str(randrange(0, 10)) for _ in range(6))
            Cofirmation.objects.create(
                type="password_reset",
                user_id=user.id,
                code=code,
                expiration_time=timezone.now() + timezone.timedelta(minutes=3)
            )
            send_code(code)
            data = {
                "success": True,
                "message": "Parolni tiklash arizasi qabul qilindi kodni tasdiqlang !"
            }
            return Response(data=data)
        else:
            data = {"success": False,
                "message": "Bunday foydalanuvchi mavjud emas"}
            raise Response(data)


class ResetPassConfirm(APIView):
    permission_classes = AllowAny,

    def post(self, request):
        phone = self.request.data.get("phone")
        password = self.request.data.get("password")
        password2 = self.request.data.get("password2")
        user = User.objects.filter(phone=phone).last()

        if password == password2:
            user.set_password(password)
            user.save()
            response = {"success": True, "message": "Parol yangilandi"}
        else:
            response = {"success": False,
                "message": "Parollar bir biriga mos emas !"}
        return Response(response)


class ResendCodeView(APIView):
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        phone = self.request.data.get("phone")
        type = self.request.data.get("type")

        if phone is None or type is None:
            return Response({"message": "Ma'lumot to'liq kiritilmadi! \n\Kerakli ma'lmotlar: ['phone', 'type']"})

        userqs = User.objects.filter(phone=phone)
        if userqs.exists():
            user = userqs.last()

            old_obj = Cofirmation.objects.filter(
                user__phone=phone, expiration_time__lte=timezone.now())
            if old_obj.exists():
                oob = old_obj.last()
                oob.delete()

            qs = Cofirmation.objects.filter(
                user__phone=phone, type=type, expiration_time__gte=timezone.now())
            if qs.exists():
                obj = qs.last()
                code = obj.code

            else:
                lists = ["register", "resend",
                    "change_phone", "password_reset", "order"]
                if type in lists:
                    code = "".join(str(randrange(0, 10)) for _ in range(6))
                    Cofirmation.objects.create(
                    type=type,
                    user_id=user.id,
                    code=code,
                    expiration_time=timezone.now() + timezone.timedelta(minutes=3)
                    )
                else:
                    return Response({"success": False, "message": "Bunday Verifikatsiya turi mavjud emas"})
            send_code(code)
            response = {"success": True,
                "message": "Kod qayta yuborildi tasdiqlang"}
            return Response(response)

        else:

            return Response({"success": False, "message": "Bunday foydalanuvchi mavjud emas"})


####################   USER MODEL  ##################################


class UploadImageApiView(CreateAPIView, generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadImageSerializer
    queryset = UploadFile.objects.all()
    

    def post(self, request, *args, **kwargs):
        try:
            file = UploadFile.objects.create(file=request.data['file'])
            return Response({"success": True, "message": "OK", "results": {"id": file.id, "url": file.url}})
        except Exception as e:
            return Response({"success": False, "message": str(e.args)}, status=status.HTTP_400_BAD_REQUEST)


class CreateProfileView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateProfileSerializer

    def get_queryset(self):
        return Profile.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        user = self.request.user
        images = self.request.data.get('images', None)
        first_name = self.request.data.get('first_name', None)
        last_name = self.request.data.get('last_name', None)
        email = self.request.data.get("email", None)

        is_images = False
        user_exists = Profile.objects.filter(user=user).exists()

        if user_exists:
            raise ValueError(
                {"success": False, "message": "Bu foydalanuvchi profili mavjud !"})
        else:
            profile = Profile.objects.create(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                email=email
            )

        def validate_image(images):
            if images is None:
                raise Response({
                    "success": False, "message": "Rasm yuklashda xatolik"
                })
            return True

        if request.data.get('images', None):
            validate_image(images=request.data.get('images', None))
            is_images = True

        if images is not None:
            set_image_profile(profile , images, is_images=is_images)

        data = {
            'success': True,
            'message': "Profil malumotlari saqlandi",
            'id':profile.id
        }
        return Response(data)


class ProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateProfileSerializer
    queryset = Profile.objects.all()
    
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.filter(id=kwargs['pk'])
        pr = profile.last()
        if profile.exists():
            data = {
                "id":pr.id,
                "first_name" : pr.first_name,
                "last_name" : pr.last_name,
                "email" : pr.email,
                "image" : pr.photo,
                "userId":pr.user_id
                }
            
            addr = Address.objects.filter(profile=pr)
            if addr.exists():
                addres = addr.last()
                data['address'] = addres.id

        else:
            data = {
                "success":False, "message":"Bunday profil mavjud emas."
            }
        return Response(data)

    def patch(self, request, *args, **kwargs):
        images = request.data.get("images", None)
        if images is not None:
            profile = Profile.objects.filter(id=kwargs['pk'])
            if profile.exists():
                set_image_profile(profile.last(), images)
        self.partial_update(request, *args, **kwargs)
        return Response({"success":True, "message":"Profil malumotlari yangilandi"})


    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({"success":True, "message":"Profil o'chirildi"})



# ------------------Address--------------------------------------------    

class AddressCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        return Address.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        profile = Profile.objects.filter(user_id=user.id)
        if profile.exists():
            serializer.save(profile=profile.last())
        else:
            return Response({"success":False, "message":"Manzil uchun profil mavjud emas"})

    def post(self, request, *args, **kwargs):
        zip_code = self.request.data.get("zip_code")
        qs = Address.objects.filter(zip_code=zip_code)
        if qs.exists():
            data = {
                "success":False, "message":"Bu manzil allaqachon qo'shilgan !"
            }
            return Response(data)



        self.create(request, *args, **kwargs)
        return Response({"success":True, "message":"Manzil malumotlari saqlandi"})



class AddressAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = IsAuthenticated,

    def get_queryset(self):
        user = self.request.user
        profile = Profile.objects.filter(user_id=user.id).last()
        return Address.objects.filter(profile_id=profile.id) 

    def patch(self, request, *args, **kwargs):
        self.partial_update(request, *args, **kwargs)
        return Response({"success":True, "message":"Manzil malumotlari yangilandi"})

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return Response({"success":True, "message":"Manzil o'chirish muvaffaqiyatli"})











