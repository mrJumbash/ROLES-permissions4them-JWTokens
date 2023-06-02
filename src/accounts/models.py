from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.settings import ROLE_CHOICES

class User(AbstractUser):
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)



class ConfirmCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField()

