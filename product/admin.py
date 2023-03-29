from django.contrib import admin
from .models import Product, ProductAttribute, ProductImage, UploadImageProduct, Attribute


admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductImage)
admin.site.register(UploadImageProduct)
admin.site.register(Attribute)
