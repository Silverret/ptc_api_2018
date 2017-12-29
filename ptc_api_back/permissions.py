"""
Custom permissions are defined here.
"""
import re
from rest_framework import permissions
from ptc_api_back.models import Trip


class IsTravelerOrIsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow owners of a trip/profile to get, post or update it.
    """
    def has_permission(self, request, view):
        return request.user and (request.user.is_staff or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.traveler == request.user) or request.user.is_staff


class IsTripTravelerOrAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow owners of a trip to edit its segments or its tasks.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                assert re.match(r'^[0-9]+$', request.data['trip'])
                cor_trip_id = int(request.data['trip'])
                cor_trip = Trip.objects.get(id=cor_trip_id)
                return request.user == cor_trip.traveler
            except (KeyError, ValueError, AssertionError):
                return False
        # For the other methods (GET, PUT, DELETE, ...)
        return request.user and (request.user.is_staff or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.trip.traveler == request.user) or request.user.is_staff


class IsUserOrIsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own account.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and (request.user.is_staff or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj == request.user) or request.user.is_staff
