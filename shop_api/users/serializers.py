from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import  CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from . import utils

class UserBaseSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    birthday = serializers.DateField()

class AuthValidateSerializer(UserBaseSerializer):
    pass


class RegisterValidateSerializer(UserBaseSerializer):
    def validate_email(self, email):
        try:
            CustomUser.objects.get(email=email)
        except:
            return email
        raise ValidationError('CustomUser уже существует!')
    
class ConfirmSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        code = attrs.get('code')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise ValidationError('CustomUser не существует!')

        if not utils.verify_confirmation_code(user.email, code):
            raise serializers.ValidationError("Неверный код подтверждения")
        attrs['user'] = user
        return attrs
    
    def save(self, **kwargs):
        user = self.validated_data['user']
        user.is_active = True
        user.save()
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
    
        authenticate_kwargs = {
            'email': attrs['email'],
            'password': attrs['password'],
        }
        self.user = authenticate(**authenticate_kwargs)
        if not self.user or not self.user.is_active:
            raise serializers.ValidationError(
                'No active account found with the given credentials'
            )
        data = super().validate(attrs)
        data['birthday'] = self.user.birthday.isoformat() if self.user.birthday else None
        return data

    
class OuathCodeSerializer(serializers.Serializer):
    code = serializers.CharField()


