from django.contrib import admin
from accounts import models

admin.site.register(models.ConfirmCode)
admin.site.register(models.TenantCode)


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "password",
        "email",
        "role",
        "is_active",
        "is_verified",
        "is_staff",
        "auth_provider",
    ]
    readonly_fields = ["id"]
    fields = ["username", "password", "role", "email", "auth_provider", "is_verified"]
