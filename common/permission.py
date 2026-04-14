from rest_framework import permissions
from rest_framework.permissions import BasePermission





class HasSubsription(permissions.BasePermission):
    message = "You must have an active subsrcition to access this"

    class HasActiveSubscription(BasePermission):
        def has_permission(self, request, view):
            user = request.user

            if not user or not user.is_authenticated:
                return False

            subscription = user.subscription_set.filter(is_active=True).first()

            return subscription is not None
        




class HasRolePermission(BasePermission):
    message = "You do not have permission to access this."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user_role = getattr(request.user.profile, "role", None)
        required_roles = getattr(view, "required_roles", [])

        return user_role in required_roles
