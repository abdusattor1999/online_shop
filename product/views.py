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
    
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    
    def get_queryset(self, object=None, category=None): 
        products = []
        images = []
        if category:
            all_queryset = Product.objects.filter(category_id=category)
        elif object:
            all_queryset = Product.objects.filter(id=object)
        else:
            all_queryset = Product.objects.all()
        
        for pr in all_queryset:
            one = {
                "id":pr.id,
                "name":pr.name,
                "category":{"id":pr.category.id, "name":pr.category.name},
                "seller":{"id":pr.seller.id, "name":pr.seller.shop_name},
                "description":pr.description,
                "price":str(pr.price),
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
            pr_atts =  ProductAttribute.objects.filter(product=pr)
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
            for image in images:
                img = UploadImageProduct.objects.filter(id=image)
                if img.exists():
                    ProductImage.objects.create(
                        inctance_id=product.id,
                        image_id=image
                    )
                else:
                    return Response({"success": False, "message": "Bunday rasm mavjud emas"})
        else:
            return Response({"success": False, "message": "Rasm yuklashda xatolik bor"})

        # Attribut set qilamiz
        # 1 - attributes listini ichidagi har bitta dict(attrs1) birxil maxsulot bo'ladi
        # 2 - har bitta attrs bitta ProductAttribute obyekti bo'ladi
        # 3 - attrs ni ichidagi har bitta dict bitta Attribute obyekti bo'ladi -> get_or_create
        # 4 - attrs ni ichida quantity degan qiymat bo'ladi u ProductAttributega quantity sifatida beriladi

        if attributes is not None:
            for attrs in attributes:
                quantity = attrs.pop("quantity", None)
                product_attr = ProductAttribute.objects.create(product=product)
                
                for name, value in attrs.items():
                    attr = Attribute.objects.filter(name=name, value=value)
                    if attr.exists():
                        attr_one = attr.last()
                    else:
                        attr_one = Attribute.objects.create(name=name, value=value)
                    product_attr.attribute.add(attr_one)
                product_attr.quantity = quantity
                product_attr.save()


        return Response({"success": True, "message": "Maxsulot saqlandi", "id":product.id})
