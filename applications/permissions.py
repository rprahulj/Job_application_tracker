from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOfApplicationRelatedObject(BasePermission):
    """Defense-in-depth permission for objects linked to an application."""
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user_id"):
            return obj.user_id == request.user.id
        return obj.application.user_id == request.user.id
