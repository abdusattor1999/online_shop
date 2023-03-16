from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given phone and password.
        """
        if not phone:
            raise ValueError(_("Telefon raqam kiritilishi shart !"))
   
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user
      

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser is_staff=True bo'lishi kerak."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser is_superuser=True bo'lishi kerak."))
        return self.create_user(phone, password, **extra_fields)