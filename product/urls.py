from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    UploadImagesAPI, ProductCrateAPI, 
    ProductEditDeleteAPI, CategoryApi,
    AttributeView , ProductViewSet )

   
urlpatterns = [
    path("post/", UploadImagesAPI.as_view(), name='images'),
    path("", ProductViewSet.as_view({"get":"list", 'post':"create",}), name='product'),
    # path("", ProductCrateAPI.as_view(), name='create'),
    # path("<int:pk>/", ProductCrateAPI.as_view(), name='get'),
    # path("<int:product>/<int:pk>/", AttributeView.as_view(), name='attribute'),
    path("categories/", CategoryApi.as_view(), name="category"),
    path("categories/<int:pk>/", CategoryApi.as_view(), name="category"),
    path("category/<int:category>/", ProductCrateAPI.as_view(), name='get_by_category'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





