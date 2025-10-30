import re
from django.contrib.auth.hashers import make_password
from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, IntegerField, CharField
from rest_framework.serializers import ModelSerializer, Serializer
from auth_user.models import User
import json


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'username', 'phone_number')

    def validate_phone_number(self, value):
        return re.sub(r'\D', '', value)

    def validate_password(self, value):
        return make_password(value)


class EmailCheckSerializer(Serializer):
    code = CharField(required=True)

    def validate_code(self, data):
        redis = Redis(decode_responses=True)
        user_data = redis.get(data)
        if not user_data:
            raise ValidationError('invalid code')
        self.user = json.loads(user_data)
        return data


class ForgotPasswordSerializer(Serializer):
    email = EmailField(max_length=255)
    confirm_password = CharField(max_length=50)
    password = CharField(max_length=50)

    def validate(self, data):
        confirm = data.get('confirm_password')
        password = data.get('password')
        email = data.get('email')
        query = User.objects.filter(email=email)
        if not query.exists():
            raise ValidationError('email not exist')
        if password != confirm:
            raise ValidationError('passwords are not equal')
        return data


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        read_only_fields = ('email',)
