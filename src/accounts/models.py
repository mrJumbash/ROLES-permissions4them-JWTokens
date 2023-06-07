from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from common.models import BaseModel
from accounts.settings import ROLE_CHOICES, AUTH_PROVIDERS
from accounts.managers import UserManager


class User(AbstractUser, BaseModel, PermissionsMixin):
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True, default=3
    )
    username = models.CharField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=255, blank=True, null=True, default=AUTH_PROVIDERS.get("email")
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return self.email


class ConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField()


class TenantCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField()
