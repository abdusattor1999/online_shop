from django.db import models
from rest_framework.response import Response

STATUS_CHOICES = {
        ("active", "active"),
        ("inactive", "inactive")
        }

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nomi")
    category = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="categ")
    icon = models.URLField(blank=True, null=True, verbose_name="Icon URL")

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Maxsulot nomi")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="product_category")
    seller = models.ForeignKey('seller.Seller', on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Ma'lumot", blank=True, null=True)
    attributes = models.ManyToManyField('AttributeValue', blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")
    discount = models.PositiveIntegerField(verbose_name="Chagirma (foizda)", blank=True, null=True)
    status = models.CharField(max_length=60, choices=STATUS_CHOICES, default='active')
    created = models.DateTimeField(auto_now_add=True)

    def get_price(self):
        if self.discount:  
            price = (self.price / 100)*(100-self.discount)
        else:
            price = self.price
        return price

    def set_properties(self, prop:dict):
        product_fields = [f.name for f in self._meta.get_fields()]
        a = self._meta.fields

        for f_name, value in prop.items():
            if f_name in product_fields:
                print("Bor")
                setattr(self, f_name, value)
        self.save()     
     

    def set_images(self, images:list, old=None):
            if old is not None:
                old_images = ProductImage.objects.filter(inctance_id=self.id)
                if old_images.exists():
                    for img in old_images:
                        img.delete()
                        # ProductImage.objects.delete(id=img.id)
            for image in images:
                img = UploadImageProduct.objects.filter(id=image)
                if img.exists():
                    ProductImage.objects.create(
                        inctance_id=self.id,
                        image_id=image
                    )
                else:
                    raise Response({"success": False, "message": "Bunday rasm mavjud emas"})

    def get_images(self):
        image_list = []
        image_objects = ProductImage.objects.filter(inctance=self)
        for img in image_objects:
            image_list.append({"id":img.image.id, "url":img.image.url})
        return image_list
    

    def set_attributes(self, attrs):
        for attr in attrs:
            attribute = Attribute.objects.filter(name=attr['name'])
            if attribute.exists():
                attribute = attribute.last()
            else:
                attribute = Attribute.objects.create(name=attr['name'])
            
            attribute_value = AttributeValue.objects.filter(attribute=attribute, value=attr['value'])
            if attribute_value.exists():
                attribute_value = attribute_value.last()
            else:
                attribute_value = AttributeValue.objects.create(attribute=attribute, value=attr['value'])

            self.attributes.add(attribute_value)
        self.save()
    
    def get_attributes(self):
        attrs_list = []
        product_atttributes = AttributeValue.objects.filter(product=self)
        for one_attr in product_atttributes:
            dicct = {one_attr.attribute.name:one_attr.value}
            print(dicct)
            attrs_list.append(dicct)
        return attrs_list

    def __str__(self):
        return str(self.name)

class UploadImageProduct(models.Model):
    image = models.FileField(upload_to="product_images/") 
    @property
    def url(self):
        if self.image:
            return self.image.url
        else:
            return None
             
    def __str__(self):
        return str(self.id)

class ProductImage(models.Model):
    inctance = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ForeignKey(UploadImageProduct, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"Product : {self.inctance.id},   Image : {self.image.id}"


class Attribute(models.Model):
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.name}"
    

class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute,on_delete=models.CASCADE, blank=True, related_name="attributes")
    value = models.CharField(max_length=30)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.value}"












