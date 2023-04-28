from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializer import (
    ProductSerializer, 
    UploadImageProductSerializer, 
    CategorySerializer, 
    AttributeSerializer )
from .models import (
    ProductImage,# ProductAttribute, 
    Attribute, Product, 
    UploadImageProduct, Category )
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

class CategoryApi(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = CategorySerializer
    
    def get_queryset(self, categ):
        if categ:
            jami_list = []
            objects = Category.objects.filter(category_id=categ)
            for i in objects:
                jami_list.append(
                    {
                    "id":i.id,
                    "name":i.name,
                    "category_id":i.category.id,
                    "icon":i.icon
                    }
                )
            return jami_list
        else:
            return super().get_queryset()
            

    def get(self, request, *args, **kwargs):
        categ_id = kwargs.get("pk", None)
        if categ_id is not None:
            return Response(self.get_queryset(categ_id))
        return super().get(request, *args, **kwargs)
  


# class ProductCrateAPI(ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView):
#     permission_classes = IsAuthenticated,
#     serializer_class = ProductSerializer
#     queryset = Product.objects.all()

#     # 1. GET
#     def get_queryset(self, object=None, category=None): 
#         products = []
#         images = []
#         if category:
#             all_queryset = Product.objects.filter(category_id=category)
#         elif object:
#             all_queryset = Product.objects.filter(id=object)
#         else:
#             all_queryset = Product.objects.all() 

#         if all_queryset.exists():
#             for pr in all_queryset:
#                 one = {
#                     "id":pr.id,
#                     "name":pr.name,
#                     "category":{"id":pr.category.id, "name":pr.category.name},
#                     "seller":{"id":pr.seller.id, "name":pr.seller.shop_name},
#                     "description":pr.description,
#                     "old_price":str(pr.price),
#                     "price":str(pr.get_price()),
#                     "discount":pr.discount,
#                     "status":pr.status,
#                     "created":str(pr.created)
#                 }
#                 # Rasmlarni listga dict holatida solib chiqamiz
#                 img_qs = ProductImage.objects.filter(inctance=pr)
#                 for img in img_qs:
#                     images.append({"id":img.id, "url":img.image.url})
#                 one["images"] = images 

#                 # Attribute qo'shamiz  
#                 pr_atts =  ProductAttribute.objects.filter(product=pr, status='active')
#                 if pr_atts.exists():
#                     list_attrs = []
#                     for one_attr in pr_atts:
#                         attr_obs = Attribute.objects.filter(many_attributes=one_attr)
#                         listga_qosh = {"id":one_attr.id}
#                         # Bir ProductAttribut obyektiga tegishli hamma Attributlarni olamiz
#                         for i in attr_obs:
#                             listga_qosh[i.name] = i.value

#                         if one_attr.quantity is not None:
#                             listga_qosh['quantity'] = one_attr.quantity
#                         list_attrs.append(listga_qosh)
#                     one['attributes'] = list_attrs

#                 products.append(one)
#             return products
#         else:
#             return Response({"success":False, "message":"Munday maxsulot mavjud emas"})
#     # 1. GET
#     def get(self, request, *args, **kwargs):
#         one_obj = kwargs.get("pk", False)
#         categ = kwargs.get("category", False)
#         if categ:
#             resp = Response(self.get_queryset(category=categ))
#         elif one_obj:
#             resp = Response(self.get_queryset(object=one_obj))
#         else:
#             resp = Response(self.get_queryset())
#         return resp



#     # 2. POST
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         # Rasmlarni , Attributlarni  ajratvolamiz
#         images = request.data.pop("images", None)
#         attributes = request.data.pop("attributes", None)
#         category = request.data.pop("category", None)
#         get_categ = Category.objects.get_or_create(name=category.title())[0]

#         seller_id = request.data.get("seller")
#         seller = Seller.objects.filter(id=seller_id)
#         if seller.exists():
#             sell = seller.last()
#         else:
#             return Response({"success":False, "message":"Bunday sotuvchi mavjud emas"})
#         # Productni saqlaymiz

#         product = Product.objects.create(
#             name=request.data.get("name"),
#             category_id=get_categ.id,
#             seller_id=sell.id,
#             description=request.data.get("description", None),
#             price=request.data.get("price"),
#             discount = request.data.get("discount", None)
#         )
#         # Rasmlarni set qilamiz
#         if images is not None:
#             product.set_images(images)
#         else:
#             return Response({"success": False, "message": "Rasm yuklashda xatolik bor"})

#         # Attributlarni qo'shamiz
#         if attributes is not None:
#             product.set_attributes(attributes)
#         return Response({"success": True, "message": "Maxsulot saqlandi", "id":product.id})

#     # 3. PATCH
#     def patch(self, request, *args, **kwargs):
#         # So'rov turlari:
#             # 1. productni o'zini malumotlarini o'zgartirish ✔️ 
#             # 2. rasmni o'zgartirish ✔️
#             # 3. yangi rasm qo'shish ✔️
#             # 7. yangi attribut qo'shish ✔️
#         product = Product.objects.get(id=kwargs['pk'])          
#         attributes = request.data.pop("attributes", None)
#         delete_old = request.data.pop("delete_old_attrs", None)

#         if attributes is not None:
#             product.set_attributes(attributes, delete_old)

#         images = request.data.pop("images", None)
#         old_images = request.data.pop("delete_old_images", None)
#         if images is not None:
#             product.set_images(images, old_images)

#         req_data = request.data
#         if len(req_data) > 0:
#             product.set_properties(req_data)
            
#         return Response({"success":True, "message":"Mahsulot malumotlari yangilandi"})



#     def delete(self, request, *args, **kwargs):
#         return super().delete(request, *args, **kwargs)


# class ProductEditDeleteAPI(RetrieveUpdateDestroyAPIView, ListAPIView):
#     permission_classes = IsAuthenticated,
#     serializer_class = ProductSerializer

    # def get_queryset(self, object=None, category=None): 
    #     products = []
    #     images = []
    #     if category:
    #         all_queryset = Product.objects.filter(category_id=category)
    #     elif object:
    #         all_queryset = Product.objects.filter(id=object)
    #     else:
    #         all_queryset = Product.objects.all() 

    #     if all_queryset.exists():
    #         for pr in all_queryset:
    #             one = {
    #                 "id":pr.id,
    #                 "name":pr.name,
    #                 "category":{"id":pr.category.id, "name":pr.category.name},
    #                 "seller":{"id":pr.seller.id, "name":pr.seller.shop_name},
    #                 "description":pr.description,
    #                 "old_price":str(pr.price),
    #                 "price":str(pr.get_price()),
    #                 "discount":pr.discount,
    #                 "status":pr.status,
    #                 "created":str(pr.created)
    #             }
    #             # Rasmlarni listga dict holatida solib chiqamiz
    #             img_qs = ProductImage.objects.filter(inctance=pr)
    #             for img in img_qs:
    #                 images.append({"id":img.id, "url":img.image.url})
    #             one["images"] = images 

    #             # Attribute qo'shamiz  
    #             pr_atts =  ProductAttribute.objects.filter(product=pr, status='active')
    #             if pr_atts.exists():
    #                 list_attrs = []
    #                 for one_attr in pr_atts:
    #                     attr_obs = Attribute.objects.filter(many_attributes=one_attr)
    #                     listga_qosh = {"id":one_attr.id}
    #                     # Bir ProductAttribut obyektiga tegishli hamma Attributlarni olamiz
    #                     for i in attr_obs:
    #                         listga_qosh[i.name] = i.value

    #                     if one_attr.quantity is not None:
    #                         listga_qosh['quantity'] = one_attr.quantity
    #                     list_attrs.append(listga_qosh)
    #                 one['attributes'] = list_attrs

    #             products.append(one)
    #         return products
    #     else:
            # return Response({"success":False, "message":"Munday maxsulot mavjud emas"})

    # def get(self, request, *args, **kwargs):
    #     one_obj = kwargs.get("pk", False)
    #     categ = kwargs.get("category", False)
    #     if categ:
    #         resp = Response(self.get_queryset(category=categ))
    #     elif one_obj:
    #         resp = Response(self.get_queryset(object=one_obj))
    #     else:
    #         resp = Response(self.get_queryset())
    #     return resp


    

    # def patch(self, request, *args, **kwargs):
    #     # So'rov turlari:
    #         # 1. productni o'zini malumotlarini o'zgartirish  
    #         # 2. rasmni o'zgartirish ✔️
    #         # 3. yangi rasm qo'shish ✔️
    #         # 7. yangi attribut qo'shish ✔️
    #     product = Product.objects.get(id=kwargs['pk'])          
    #     attributes = request.data.pop("attributes", None)
    #     delete_old = request.data.pop("delete_old_attrs", None)

    #     if attributes is not None:
    #         product.set_attributes(attributes, delete_old)

    #     images = request.data.pop("images", None)
    #     old_images = request.data.pop("delete_old_images", None)
        
    #     if images is not None:
    #         product.set_images(images, old_images)
    #     req_data = request.data
    #     if len(req_data) > 0:
    #         product.set_properties(req_data)
            
    #     return Response({"success":True, "message":"Mahsulot malumotlari yangilandi"})


class AttributeView(RetrieveUpdateDestroyAPIView):
    permission_classes = IsAuthenticated,
    serializer_class = AttributeSerializer
    queryset = Attribute.objects.all()

    # 1. attributni inactive qilish ✔️
    # 2. attributni o'chirish ✔️
    # 3. maxsulotni qaysidur attributini sonini o'zgartirish ✔️
    
    def get(self, request, *args, **kwargs):
        attribute = self.queryset.get(id=kwargs['pk'])
        resp = {
            "id":attribute.id,
            "product_id":attribute.product.id,
        }
        ichki_attrs = Attribute.objects.filter(many_attributes=attribute)
        for i in ichki_attrs:
            resp[i.name]=i.value
        resp["quantity"] = attribute.quantity
        resp["status"] = attribute.status

        return Response(resp)


    def patch(self, request, *args, **kwargs):
        object = self.queryset.get(id=kwargs['pk'])
        status = request.data.get("status", False)
        quantity = request.data.get("quantity", False)
        if status:
            object.status = status
        if quantity:
            object.quantity = quantity
        object.save()

        return Response({"success":True, "message":"Attribute yangiandi", "details":request.data})
    
    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"success":True, "message":"Attribute deleted successfully"}) 
##########################################################################################

from rest_framework.viewsets import ModelViewSet

class ProductViewSet(ModelViewSet):
    permission_classes = IsAuthenticated,
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        attributes = request.data.pop("attributes", False)
        images = request.data.pop('images', False)

        product = Product.objects.create(**serializer.validated_data)

        if attributes:
            print(attributes)
            product.set_attributes(attributes)
        if images:
            print(images)
            product.set_images(images)

        return Response({"success":True, "message":"Maxsulot saqlandi", "id":product.id})
                                                        

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        data['images']=instance.get_images()
        data['attributes']=instance.get_attributes()

        instance.view += 1
        instance.save()

        return Response(data)
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        images = request.data.pop('images', False)
        attributes = request.data.pop("attributes", False)
        product = Product.objects.get(id=kwargs['pk'])

        if images:
            product.set_images(images)
        if attributes:
            product.set_attributes(attributes)

        self.update(request, *args, **kwargs)
        return Response({"success":True, "message":"Informations have been updated."})