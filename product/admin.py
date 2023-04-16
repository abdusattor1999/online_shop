from django.contrib import admin
from .models import Product, Category ,ProductImage, UploadImageProduct, Attribute


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "seller","price", "status", "created")

@admin.register(UploadImageProduct)
class ImageUploadProductAdmin(admin.ModelAdmin):
    list_display = ("id", "url")

# @admin.register(ProductAttribute)
# class ProductAttributeAdmin(admin.ModelAdmin):
#     fields = ['product', "attribute"]
#     list_display = ("product","get_related_objects", "quantity","status")

#     # def get_attrs(self, obj):
#     #     return "\n".join([p for p in obj.attribute])

#     def get_related_objects(self, obj):
#         return "\n".join([f"{attr.name} : {attr.value}" for attr in obj.attribute.all()])
#     get_related_objects.short_description = 'Related Objects'


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name", "status")

@admin.register(ProductImage)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("inctance", "image")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name", "category", "icon")
