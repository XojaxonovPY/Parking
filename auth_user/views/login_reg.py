import random
import json
from http import HTTPStatus

from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from redis import Redis
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from root.settings import EMAIL_HOST_USER
from auth_user.models import User
from auth_user.serialize import RegisterModelSerializer, EmailCheckSerializer, ForgotPasswordSerializer
from auth_user.task import send_email


@extend_schema(request=RegisterModelSerializer, responses=RegisterModelSerializer, tags=['auth'])
@api_view(['POST'])
@permission_classes([AllowAny])
def register_api_view(request):
    serializer = RegisterModelSerializer(data=request.data)
    code = str(random.randrange(10 ** 5, 10 ** 6))
    if serializer.is_valid():
        email = serializer.validated_data.get('email')
        redis = Redis()
        redis.mset({code: json.dumps(request.data)})
        send_email.delay(
            subject="Verification Code !!!",
            message=f"{code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email]
        )
        return Response({'message': 'Verify code'}, status=HTTPStatus.CREATED)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@extend_schema(request=EmailCheckSerializer, responses=EmailCheckSerializer, tags=['auth'])
@api_view(['POST'])
@permission_classes([AllowAny])
def email_check_api_view(request):
    serializer = EmailCheckSerializer(data=request.data)
    if serializer.is_valid():
        User.objects.create(**serializer.user)
        return Response({'message': 'Email is verified'}, status=HTTPStatus.OK)
    return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


@extend_schema(request=ForgotPasswordSerializer, responses=ForgotPasswordSerializer, tags=['auth'])
@api_view(['PATCH'])
@permission_classes([AllowAny])
def forgot_password_ap_view(request):
    serialize = ForgotPasswordSerializer(data=request.data)
    if serialize.is_valid():
        password = serialize.validated_data.get('password')
        email = serialize.validated_data.get('email')
        User.objects.filter(email=email).update(password=make_password(password))
        return JsonResponse({'new_password': password}, status=HTTPStatus.OK)
    else:
        return Response(serialize.errors, HTTPStatus.BAD_REQUEST)


# =====================================================auth-jwt

@extend_schema(tags=['auth'])
class CustomerTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(tags=['auth'])
class CustomerTokenRefreshView(TokenRefreshView):
    pass
