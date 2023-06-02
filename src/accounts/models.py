from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    ADMIN = 1
    TENANT = 2
    BUYER = 3

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (TENANT, 'tenant'),
        (BUYER, 'buyer')
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)



class ConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField()

