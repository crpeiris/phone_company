from django.contrib.auth.models import Permission
from .models import Staff, Role, Order

class IsHelpDesk(Permission):
    """Allow access only to users with help desk role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='help_desk').exists()

class IsOrderManager(Permission):
    """Allow access only to users with order manager role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='order_manager').exists()

class IsGeneralManager(Permission):
    """Allow access only to users with general manager role."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='general_manager').exists()
