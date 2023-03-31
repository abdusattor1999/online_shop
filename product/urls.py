from django.urls import path
from .views import UploadImagesAPI, ProductCrateAPI


urlpatterns = [
    path("images/", UploadImagesAPI.as_view(), name='images'),
    path("", ProductCrateAPI.as_view(), name='create'),
]