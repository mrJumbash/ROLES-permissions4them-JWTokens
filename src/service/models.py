from django.db import models
from common.models import BaseModel
from accounts.models import User

class Product(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name='Заголовок'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    models.PositiveIntegerField
    
    price = models.FloatField(
        verbose_name='Цена'
    )

    owner = models.OneToOneField(User, on_delete=models.CASCADE)


