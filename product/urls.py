from django.urls import path
from .views import UploadImagesAPI, ProductCrateAPI, ProductEditDeleteAPI, CategoryApi
from django.conf import settings
from django.conf.urls.static import static
   
urlpatterns = [
    path("images/", UploadImagesAPI.as_view(), name='images'),
    path("", ProductCrateAPI.as_view(), name='create'),
    path("<int:pk>/", ProductEditDeleteAPI.as_view(), name='get'),
    path("categories/", CategoryApi.as_view(), name="category"),
    path("categories/<int:pk>/", CategoryApi.as_view(), name="category"),
    path("category/<int:category>/", ProductCrateAPI.as_view(), name='get_by_category'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





