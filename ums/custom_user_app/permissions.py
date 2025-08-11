# custom_user_app/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdmin(BasePermission):
    """Allow only admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsFaculty(BasePermission):
    """Allow only faculty."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'faculty'


class IsStudent(BasePermission):
    """Allow only students."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'student'


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission: allow admin or the owner of the object.
    Owner detection works for models with `.user` or `.student.user`.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        owner = getattr(obj, 'user', None)
        if owner is None and hasattr(obj, 'student'):
            owner = getattr(obj.student, 'user', None)
        return owner == request.user
