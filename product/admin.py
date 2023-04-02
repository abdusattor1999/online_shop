from django.contrib import admin
from .models import Product, ProductAttribute, Category ,ProductImage, UploadImageProduct, Attribute


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "seller","price", "status", "created")

@admin.register(UploadImageProduct)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "url")

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    fields = ['product', "attribute"]
    list_display = ("product","get_related_objects", "quantity","status")

    # def get_attrs(self, obj):
    #     return "\n".join([p for p in obj.attribute])

    def get_related_objects(self, obj):
        return "\n".join([f"{attr.name} : {attr.value}" for attr in obj.attribute.all()])
    get_related_objects.short_description = 'Related Objects'


@admin.register(Attribute)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "value", "status")

@admin.register(ProductImage)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("inctance", "image")

@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "icon")
