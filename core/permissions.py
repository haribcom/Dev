"""
Customized permission classes for Authentication
"""
from rest_framework import permissions


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    """
    Customized permission for logged in user or admin
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user and request.user.is_staff


class IsAdminUser(permissions.BasePermission):
    """
    Permission given only for admin user
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
