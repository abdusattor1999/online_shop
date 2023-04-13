from django.db import models
from account.models import User, UploadFile

 

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=60, verbose_name="Egasi ismi")
    last_name = models.CharField(max_length=60, verbose_name="Egasi familiyasi")
    surname = models.CharField(max_length=60, verbose_name="Otasining ismi")
    shop_name = models.CharField(max_length=200, verbose_name="Do'kon nomi")

    inn = models.CharField(max_length=15, verbose_name="INN raqami")
    bank_mfo = models.CharField(max_length=8, verbose_name="Bank MFO raqami")
    bank_account = models.CharField(max_length=30, verbose_name="Bank hisob raqami")

    email = models.EmailField(unique=True, verbose_name="Email pochtasi")
    bio = models.TextField(null=True, blank=True, verbose_name="Bio")
    address = models.CharField(max_length=250, null=True, blank=True, verbose_name="Manzil")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")


    def set_image(self, images:list):
        # set image for user
        for image_id in images:
            print("image setted from models")
            ShopPictures.objects.create(instance_id=self.id, image_id=image_id)

    def get_image(self):
        image_qs = ShopPictures.objects.filter(instance_id=self.id)
        if image_qs.exists():
            img = image_qs.last()
            data = {"id":img.id, "url":img.url}
        else:
            data = None
        return data


    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def __str__(self):
        return f"{self.shop_name} : {self.id}" 
    



class ShopPictures(models.Model):
    instance = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="shop")
    image = models.ForeignKey(UploadFile, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
    @property
    def url(self):
        if self.image:
            return self.image.file.url
        else:
            return None
    