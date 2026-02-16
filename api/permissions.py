from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Only event creator can edit/delete their event"""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.creator == request.user