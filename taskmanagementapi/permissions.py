from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='admin').exists()

class IsManager(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.groups.filter(name='manager').exists()

class IsUser(BasePermission):
    def has_permission(self,request,view):
        return request.user.is_authenticated and request.user.groups.filter(name='user').exists()

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:  # ['GET', 'HEAD', 'OPTIONS']
            return True  # Allow read-only access
        return hasattr(obj, 'user') and obj.user == request.user


