from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import ProductSerializer, UploadImageProductSerializer
from .models import ProductImage, ProductAttribute, Attribute, Product, UploadImageProduct, Category
from seller.models import Seller

class UploadImagesAPI(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadImageProductSerializer

    def post(self, request, *args, **kwargs):
        print("Ishla yaxshimi ?")
        try:
            images = request.FILES.values()
            img_id_list = []
            if images:
                for img in images:
                    file = UploadImageProduct.objects.create(image=img)
                    img_id_list.append(file.id)
                return Response({"success": True, "message": "Rasmlar yuklandi", "results": img_id_list})
            else:
                return Response({"success": False, "message": "So'rov tarkibida rasm yo'q"})
        except Exception as e:
            return Response({"success": False, "message": str(e.args)})


class ProductCrateAPI(ListCreateAPIView, ListAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Rasmlarni , Attributlarni  ajratvolamiz
        images = request.data.pop("images", None)
        attributes = request.data.pop("attributes", None)
        category = request.data.pop("category", None)
        get_categ = Category.objects.get_or_create(name=category.lower())[0]

        seller_id = request.data.get("seller_id")
        seller = Seller.objects.filter(id=seller_id)
        if seller.exists():
            sell = seller.last()
        else:
            return Response({"success":False, "message":"Bunday sotuvchi mavjud emas"})
        # Productni saqlaymiz

        product = Product.objects.create(
            name=request.data.get("name"),
            category_id=get_categ.id,
            seller_id=sell.id,
            description=request.data.get("description", None),
            price=request.data.get("price"),
            discount = request.data.get("discount", None)
        )

        # Rasmlarni set qilamiz
        if images is not None:
            product.set_images(images)
        else:
            return Response({"success": False, "message": "Rasm yuklashda xatolik bor"})

        # Attributlarni qo'shamiz
        if attributes is not None:
            product.set_attributes(attributes)

        return Response({"success": True, "message": "Maxsulot saqlandi", "id":product.id})



class ProductEditDeleteAPI(RetrieveUpdateDestroyAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = ProductSerializer

    def get_queryset(self, object=None, category=None): 
        products = []
        images = []
        if category:
            all_queryset = Product.objects.filter(category_id=category, status='active')
        elif object:
            all_queryset = Product.objects.filter(id=object, status='active')
        else:
            all_queryset = Product.objects.filter(status='active')
        
        if all_queryset.exists:

            for pr in all_queryset:
                one = {
                    "id":pr.id,
                    "name":pr.name,
                    "category":{"id":pr.category.id, "name":pr.category.name},
                    "seller":{"id":pr.seller.id, "name":pr.seller.shop_name},
                    "description":pr.description,
                    "old_price":str(pr.price),
                    "price":str(pr.get_price()),
                    "discount":pr.discount,
                    "status":pr.status,
                    "created":str(pr.created)
                }

                # Rasmlarni listga dict holatida solib chiqamiz
                img_qs = ProductImage.objects.filter(inctance=pr)
                for img in img_qs:
                    images.append({"id":img.id, "url":img.image.url})
                one["images"] = images 

                # Attribute qo'shamiz  
                pr_atts =  ProductAttribute.objects.filter(product=pr, status='active')
                if pr_atts.exists():
                    list_attrs = []
                    for one_attr in pr_atts:
                        attr_obs = Attribute.objects.filter(many_attributes=one_attr)
                        listga_qosh = {}
                        # Bir ProductAttribut obyektiga tegishli hamma Attributlarni olamiz
                        for i in attr_obs:
                            listga_qosh[i.name] = i.value

                        if one_attr.quantity is not None:
                            listga_qosh['quantity'] = one_attr.quantity
                        list_attrs.append(listga_qosh)
                    one['attributes'] = list_attrs

                products.append(one)
            return products
        else:
            return Response({"success":False, "message":"Munday maxsulot mavjud emas"})

    def get(self, request, *args, **kwargs):
        one_obj = kwargs.get("pk", False)
        categ = kwargs.get("category", False)
        if categ:
            resp = Response(self.get_queryset(category=categ))
        elif one_obj:
            resp = Response(self.get_queryset(object=one_obj))
        else:
            resp = Response(self.get_queryset())
        return resp




    def patch(self, request, *args, **kwargs):
        product = Product.objects.get(id=kwargs['pk'])          
        attributes = self.request.data.pop("attributes", None)
        delete_old = self.request.data.pop("delete_old_attrs", None)

        if attributes is not None:
            product.set_attributes(attributes, delete_old)

        images = self.request.data.pop("images", None)
        old_images = self.request.data.pop("delete_old_images", None)
        if images is not None:
            product.set_images(images, old_images)

        self.partial_update(request, *args, **kwargs)
        
        return Response({"success":True, "message":"Mahsulot malumotlari yangilandi"})
