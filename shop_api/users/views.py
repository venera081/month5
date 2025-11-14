from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserAuthSerializer, UserCreateSerializer
from django.core.mail import send_mail
import random
from .models import EmailConfirmCode

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data=serializer.errors)
    
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    user = User.objects.create_user(username=username,
                                    password=password,
                                    email=email,
                                    is_active=False)
    
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    EmailConfirmCode.objects.create(user=user, code=code)

    send_mail(
        subject='Ваш код потверждения',
        message=f'Ваш код подтверждения: {code}',
        from_email='твоя почта@mail.kg',
        recipient_list=[email],
        fail_silently=False,
    )
    print(code)
    return Response(
        data={'message': 'Код подтверждения отправлен на email.'},
        status=status.HTTP_201_CREATED)
    

@api_view(['POST'])
def confirm_email(request):
    email = request.data.get('email')
    code = request.data.get('code')

    try:
        user = User.objects.get(email=email)
        confirm_code = EmailConfirmCode.objects.get(user=user)

        if confirm_code.code == code:
            user.is_active = True
            user.save()
            confirm_code.delete()
            return Response({'message': 'Email успешно подвержден!'}, 
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неверный код'}, 
                            status=status.HTTP_400_BAD_REQUEST)
    except (User.DoesNotExist, EmailConfirmCode.DoesNotExist):
        return Response({'error': 'Пользователь или код не найден'}, 
                        status=status.HTTP_404_NOT_FOUND)



@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)
    

