import re
from django.contrib.auth.hashers import make_password
from redis import Redis
from rest_framework.exceptions import ValidationError
from rest_framework.fields import EmailField, IntegerField, CharField
from rest_framework.serializers import ModelSerializer, Serializer
from auth_user.models import User


class RegisterModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'username', 'phone_number')

    def validate_phone_number(self, value):
        return re.sub(r'\D', '', value)

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class EmailCheckSerializer(Serializer):
    email = EmailField(max_length=255)
    code = IntegerField()

    def validate(self, data):
        email = data.get('email')
        code = str(data.get('code'))

        redis = Redis(decode_responses=True)
        user = User.objects.filter(email=email).first()
        stored_code = redis.get(user.email)
        if stored_code is None:
            raise ValidationError("Verification code has expired or is invalid")

        if stored_code != code:
            raise ValidationError("Invalid verification code")
        user.is_verify = True
        user.save()
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
