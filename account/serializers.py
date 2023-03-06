from .models import User, Profile, ProfilePictures, UploadFile
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError



###---------------- User Model  -------------------------------------
class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token':"No'tog'ri token kiritildi",
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")

###---------------- User Model  -------------------------------------


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ("file",)

class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:    
        model = ProfilePictures
        fields = ('image',)



class CreateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ("first_name","last_name", "photo", "email")


