from django.urls import path
from account.views import (
    SignupView, VerifyView, LoguotView,
    UploadImageApiView, CreateProfileView , ChangePasswordView , ResendCodeView,
    ChangePhoneView, DeleteUserView, ResetPassRequestView, ResetPassConfirm
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

    path('change-phone/', ChangePhoneView.as_view(), name='change_phone'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),

    path('user/delete/<int:pk>/', DeleteUserView.as_view(), name='user-delete'),
    path("reset-password/", ResetPassRequestView.as_view(), name="request-reset-pass"),
    path("reset-verify/", VerifyView.as_view(), name="verify-reset-pass"),
    path("send-resetted/", ResetPassConfirm.as_view(), name="reset-pass-done"),
    path("resend-code/", ResendCodeView.as_view(), name="resnd_code"),

#___Profile________________________________________________________________________________________________________
    path("upload-image/", UploadImageApiView.as_view(), name="upload_image"),
    path("profile/create/", CreateProfileView.as_view(), name="pr_create")
]




