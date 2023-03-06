from django.urls import path
from account.views import (
    SignupView, VerifyView, LoguotView,
    UploadImageApiView, CreateProfileView 
    
    )

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path("token/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('verify/', VerifyView.as_view(), name='verify'),
    path('logout/', LoguotView.as_view(), name='logout'),

#___Profile________________________________________________________________________________________________________
    path("upload-image/", UploadImageApiView.as_view(), name="upload_image"),
    path("profile/create/", CreateProfileView.as_view(), name="pr_create")
]





