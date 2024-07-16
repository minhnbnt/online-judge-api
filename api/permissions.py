from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    def has_permission(self, request, _):
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    def has_object_permission(self, request, _, obj):
        return obj.owner == request.user
