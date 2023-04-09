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
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narxi")
    discount = models.PositiveIntegerField(verbose_name="Chagirma (foizda)", blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')
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

    def set_attributes(self, attributes:list, old=None):
        if old is not None:
            old_attributes = ProductAttribute.objects.filter(product=self)
            if old_attributes.exists():
                for i in old_attributes:
                    # ProductAttribute.objects.delete(id=i.id)
                    i.delete()
        # Attribut set qilamiz
        # 1 - attributes listini ichidagi har bitta dict(attrs1) birxil maxsulot bo'ladi
        # 2 - har bitta attrs bitta ProductAttribute obyekti bo'ladi
        # 3 - attrs ni ichidagi har bitta dict bitta Attribute obyekti bo'ladi -> get_or_create
        # 4 - attrs ni ichida quantity degan qiymat bo'ladi u ProductAttributega quantity sifatida beriladi

        for attrs in attributes:
            quantity = attrs.pop("quantity", None)
            product_attr = ProductAttribute.objects.create(product=self)
            for name, value in attrs.items():
                attr = Attribute.objects.filter(name=name, value=value)
                print(attr)
                if attr.exists():
                    attr_one = attr.last()
                    print("Attr_one", attr_one)
                else:
                    attr_one = Attribute.objects.create(name=name, value=value)
                product_attr.attribute.add(attr_one)
            product_attr.quantity = quantity
            product_attr.save()

            


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
    value = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.name} ({self.value})"

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, related_name="product_attributes", on_delete=models.CASCADE)
    attribute = models.ManyToManyField(Attribute, blank=True, related_name="many_attributes")
    quantity = models.PositiveIntegerField(verbose_name="Miqdori", blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.product.name}"












