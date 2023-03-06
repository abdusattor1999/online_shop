from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from random import randrange
from .utils import send_code
from datetime import datetime, timedelta
from django.utils import timezone
from .managers import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from PIL import Image
from rest_framework.response import Response



class Address(models.Model):
    user = models.ForeignKey('account.Profile', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='Manzil sarlavhasi', blank=True, null=True)
    province = models.CharField(max_length=50, verbose_name='Viloyat')
    district = models.CharField(max_length=50, verbose_name='Tuman / Shahar')
    street = models.CharField(max_length=150, verbose_name="Ko'cha nomi va uy raqami")
    zip_code = models.IntegerField(verbose_name='Pochta indexi')

    def __str__(self):
        return f"{self.title} {self.province} ({self.zip_code})"


class User(AbstractBaseUser,PermissionsMixin):

    phone = models.CharField(max_length=64, verbose_name="Telefon", unique=True)
    activated_date = models.DateTimeField(blank=True, null=True, verbose_name='Activlashgan Vaqti')
    is_seller = models.BooleanField(default=False, verbose_name="Sotuvchi holati")
    is_active = models.BooleanField(default=False, verbose_name='Activligi')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return str(self.phone)

class Cofirmation(models.Model):
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, related_name='verify_codes')
    code = models.CharField(max_length=6)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    expiration_time = models.DateTimeField(editable=None, verbose_name="Muddati")
    is_confirmed = models.BooleanField(default=False, verbose_name="Tasdiqlangan")
    
    def __str__(self):
        return str(self.user.__str__())
    
    def activate(self):
        self.is_confirmed = True
        self.save()

        user = self.user
        user.is_active = True
        user.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    photo = models.ForeignKey('account.ProfilePictures', verbose_name="Profil rasmi", blank=True, null=True, on_delete=models.CASCADE, related_name="profile_picture")
    first_name = models.CharField(max_length=50, verbose_name="Ism", blank=True, null=True)
    last_name = models.CharField(max_length=50, verbose_name="Familiya", blank=True, null=True)
    email = models.EmailField(max_length=120, null=True, blank=True, verbose_name="Email")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Ro'yxatdan o'tgan vaqti")


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def photo(self):
        qs = ProfilePictures.objects.filter(instance_id=self.id)
        if qs.exists():
            obj = qs.latest('id')
            return {"id": obj.image.id, "url": obj.image.url}
        else:
            return None
        return


    def set_photo(self, photo_id):
        object = ProfilePictures.objects.filter(instance_id=self.id)
        object.photo_id = photo_id
        object.save()
        return True


class UploadFile(models.Model):
    file = models.FileField(upload_to='upload/')

    def __str__(self):
        return str(self.id)
    
    @property
    def url(self):
        if self.file:
            return self.file.url
        else:
            return None
    

class ProfilePictures(models.Model):
    instance = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile_picture")
    image = models.ForeignKey(UploadFile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
    @property
    def url(self):
        if self.image:
            return self.image.file.url
        else:
            return None
    



@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if created:
        code = "".join(str(randrange(0,10)) for _ in range(6))
        Cofirmation.objects.create(
            user_id=instance.id,
            code=code,
            expiration_time=timezone.now() + timezone.timedelta(minutes=3)
        )
        try:
            send_code(code)
        except:
            print("Kod yuborilmadi ! ")

