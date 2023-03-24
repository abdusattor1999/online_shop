from django.urls import path
from .views import SellerEditView


urlpatterns = [
    path("", SellerEditView.as_view(), name="create-seller"),
    path("<int:pk>/", SellerEditView.as_view(), name="edit-seller")
]













