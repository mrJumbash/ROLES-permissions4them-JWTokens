from rest_framework import permissions


class IsTenantAndAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_anonymous is True:
            return False

        if request.user and request.user.role == 2:
            return True

        return bool(request.user and request.user.is_staff and request.user.role == 1)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
