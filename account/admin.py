from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User, Profile, Address, Cofirmation, ProfilePictures, UploadFile



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ("phone", "is_staff", "is_active",)
    list_filter = ("phone", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "phone", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ("phone",)
    ordering = ("phone",)


admin.site.register(User, CustomUserAdmin)



@admin.register(Address)
class AdresAdmin(admin.ModelAdmin):
    list_display = ("title", "profile", "country" , "province","district","zip_code")

@admin.register(Cofirmation)
class ConfirmAdmin(admin.ModelAdmin):
    list_display = ("user","code","created_time","expiration_time","is_confirmed")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","user","email","created_time")

admin.site.register(ProfilePictures)
admin.site.register(UploadFile)
