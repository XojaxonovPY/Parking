from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db.models import Model, EmailField, CharField, TextChoices, DateTimeField, FileField
from django.db.models.fields import BooleanField


class CustomUserManager(UserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class RoleType(TextChoices):
        OPERATOR = 'operator', "Operator"
        USER = 'user', "User"
        ADMIN = 'admin', "Admin"

    username = CharField(max_length=30, null=True, blank=True)
    email = EmailField(unique=True, null=True)
    phone_number = CharField(max_length=20, null=True, blank=True)
    password = CharField(max_length=128, null=True, blank=True)
    role = CharField(max_length=30, choices=RoleType, default=RoleType.USER)
    created_at= DateTimeField(auto_now_add=True,null=True)
    is_verify=BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()




