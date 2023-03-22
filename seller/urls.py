from django.urls import path
from .views import CreateSellerView, SellerEditView, SellerDeleteView


urlpatterns = [
    path("create/", CreateSellerView.as_view(), name="create-seller"),
    path("edit/<int:pk>/", SellerEditView.as_view(), name="edit-seller"),
    path("delete/<int:pk>/", SellerDeleteView.as_view(), name="delete-seller"),
]













