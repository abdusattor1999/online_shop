from django.db import models


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












