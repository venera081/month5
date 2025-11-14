from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username 
        raise ValidationError('username already exists!')
    
    def validate_email(self, email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise ValidationError('email alresdy exists!')