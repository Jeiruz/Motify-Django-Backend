from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from .models import Account
from django.contrib.auth.backends import ModelBackend
from drf_extra_fields.fields import Base64ImageField

# User Serializers
class UserSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Account
        fields = ["id", "username", "email", "image"]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        
        return image

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Account.objects.create_user(validated_data
        ['username'], validated_data['email'],
        validated_data['password'])
        #  it turns out that you already solve it J. if the error goes again then uncomment the thing below.
        # user.set_password(validated_data['password'])

        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")




# class CustomBackend(ModelBackend):
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=email)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None


class UpdateAccountSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = Account
        fields = ["image"]