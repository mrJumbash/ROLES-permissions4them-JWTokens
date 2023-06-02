from django.contrib import admin
from accounts import models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "password", "role"]
    readonly_fields = ["id"]
    fields = ["username", "password", "role"]
