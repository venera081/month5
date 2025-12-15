from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from users.models import CustomUser
from .serializers import RegisterValidateSerializer, AuthValidateSerializer, ConfirmSerializer
from users.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from . import utils


from users.tasks import save_random_code, send_welcome_email

class AuthorizationAPIView(CreateAPIView):
    serializer_class = AuthValidateSerializer

    def post(self, request):
        serializer = AuthValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            if not user.is_active:
                return Response(
                    status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User account is not activated yet!'}
                )

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'key': token.key})

        return Response(
            status=status.HTTP_401_UNAUTHORIZED,
            data={'error': 'User credentials are wrong!'}
        )


class RegistrationAPIView(CreateAPIView):
    serializer_class = RegisterValidateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        birthday = serializer.validated_data['birthday']

        with transaction.atomic():
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                birthday=birthday,
                is_active=False
            )

            
            code = utils.generate_confirmation_code()
            utils.save_code_to_cache(user.email, code)
            print("Code generated and saved to cache")

        
            save_random_code.delay(user.id)

            
            send_welcome_email.delay(user.email)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                'user_id': user.id,
                'confirm_code': code
            }
        )


class ConfirmUserAPIView(CreateAPIView):
    serializer_class = ConfirmSerializer

    def post(self, request):
        serializer = ConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        with transaction.atomic():
            user = CustomUser.objects.get(id=user_id)
            user.is_active = True
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

        return Response(
            status=status.HTTP_200_OK,
            data={
                'message': 'User аккаунт успешно активирован',
                'key': token.key
            }
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
