from django.contrib import admin
from service import models
from django.db.models import QuerySet
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "price", 'id']
    readonly_fields = ["created_at", "id"]
    fields = ["title", "description", "price", "created_at", 'owner']

