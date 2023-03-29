from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import ProductSerializer, UploadImageSerializer
from .models import ProductImage, ProductAttribute, Attribute, Product, UploadImageProduct


class UploadImagesAPI(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadImageSerializer

    def post(self, request, *args, **kwargs):
        try:
            images = request.FILES
            img_id_list = []
            if images:
                for img in images:
                    file = UploadImageProduct.objects.create(image=img)
                    img_id_list.append(file.id)
                return Response({"success": True, "message": "Rasmlar yuklandi", "results": img_id_list})
            else:
                return Response({"success":False, "message":"So'rov tarkibida rasm yo'q"})
        except Exception as e:
            return Response({"success": False, "message": str(e.args)})




class ProductCrateAPI(ListCreateAPIView):
    permission_classes = IsAuthenticated, 
    serializer_class = ProductSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Rasmlarni , Attributlarni  ajratvolamiz
        images = request.data.pop("images", None)
        attributes = request.data.pop("attributes", None)
        
        # Productni saqlaymiz
        product = Product.objects.create(request, *args, **kwargs)

        # Rasmlarni set qilamiz
        if images is not None:
            for image in images:
                img = UploadImageProduct.objects.filter(id=image)
                if img.exists():
                    ProductImage.objects.create(
                        inctance_id = product.id,
                        image_id = image
                    )
                else:
                    return Response({"success":False, "message":"Bunday rasm mavjud emas"})
        else:
            return Response({"success":False, "message":"Rasm yuklashda xatolik bor"})

        # Attribut set qilamiz
        # 1 - attributes listini ichidagi har bitta dict(attrs1) birxil maxsulot bo'ladi
        # 2 - har bitta attrs bitta ProductAttribute obyekti bo'ladi
        # 3 - attrs ni ichidagi har bitta dict bitta Attribute obyekti bo'ladi -> get_or_create
        # 4 - attrs ni ichida quantity degan qiymat bo'ladi u ProductAttributega quantity sifatida beriladi 

# "attributes":[
#     {
#         "colour":"white",
#         "size":"XS",
#         "quantity":25
#     },
#     {
#         "colour":"green",
#         "size":"XL",
#         "quantity":20
#     },
#     {
#         "colour":"white",
#         "size":"XXL",
#         "quantity":25
#     }
# ]

        if attributes is not None:
            for attrs in attributes:
                quantity = attrs.pop("quantity", None)
                product_attr = ProductAttribute.objects.create(product=product)
                for name, value in attrs:
                    attr = Attribute.objects.get_or_create(name=name, value=value)
                    product_attr.attribute.add(attr)
                if quantity is not None:
                    product_attr.quantity = quantity
                    product_attr.save()

        return Response({"success":True, "message":"Maxsulot saqlandi"})
                      

        