"""
Custom permissions are defined here.
"""
from rest_framework import permissions
from ptc_api_back.models import Trip
from django.contrib.auth.models import User

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a trip/profile to edit it.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            traveler_id = request.data['traveler'].split("/")[-2]
            if traveler_id is not None:
                traveler = User.objects.get(id=traveler_id)
                return request.user == traveler
        except KeyError:
            return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.traveler == request.user

class IsOwnerOfTheTripOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a trip to edit its segments or its tasks.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            print("perm: SAFE_METHODS")
            return True
        try:
            cor_trip_id = request.data['trip'].split("/")[-2]
            if cor_trip_id is not None:
                cor_trip = Trip.objects.get(id=cor_trip_id)
                print("perm: User check ", request.user == cor_trip.traveler)
                return request.user == cor_trip.traveler
        except KeyError:
            print("perm: KEY ERROR")
            return False
        return False

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        print("obj_perm: User check ", obj.trip.traveler == request.user)
        return obj.trip.traveler == request.user

class IsUserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own account.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj == request.user
