from django.urls import path
from .views import CreateSellerView, SellerEditView


urlpatterns = [
    path("", CreateSellerView.as_view(), name="create-seller"),
    path("<int:pk>/", SellerEditView.as_view(), name="edit-seller")
]













