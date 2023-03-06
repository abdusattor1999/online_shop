from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("phone",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("phone",)