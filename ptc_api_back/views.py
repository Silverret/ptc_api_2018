"""
Viewsets of the API are defined here
"""
import re

from django.contrib.auth.models import User

from rest_framework import permissions, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

from ptc_api_back.models import Trip, Segment, Task, Profile, Country, Airport
from ptc_api_back.permissions import IsUserOrIsAdminUser, IsTravelerOrIsAdminUser, IsTripTravelerOrAdminUser
from ptc_api_back.serializers import UserSerializer, ProfileSerializer, TripSerializer, SegmentSerializer
from ptc_api_back.serializers import TaskSerializer, CountryListSerializer, CountrySerializer, AirportSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTripTravelerOrAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Task.objects.all()
        return Task.objects.filter(trip__in=Trip.objects.filter(traveler=user))

    def perform_create(self, serializer):
        """
        We try to get the trip specified in the initial data
        """
        try:
            cor_trip = Trip.objects.get(id=serializer.initial_data['trip'])
        except Trip.DoesNotExist:
            cor_trip = Trip.objects.get(id=0)

        serializer.save(trip=cor_trip)


class SegmentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Segment.objects.all()
    serializer_class = SegmentSerializer
    permission_classes = [IsTripTravelerOrAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Segment.objects.all()
        return Segment.objects.filter(trip__in=Trip.objects.filter(traveler=user))

    def perform_create(self, serializer):
        """
        We try to get the trip specified in the initial data
        """
        try:
            cor_trip = Trip.objects.get(id=serializer.initial_data['trip'])
        except Trip.DoesNotExist:
            cor_trip = Trip.objects.get(id=0)

        serializer.save(trip=cor_trip)


class TripViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [IsTravelerOrIsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Trip.objects.all()
        return Trip.objects.filter(traveler=user)

    def perform_create(self, serializer):
        d_country = self.request.data['departure_country']
        a_country = self.request.data['arrival_country']
        if not bool(re.match(r'^[a-zA-Z\(\)\s,\'\-\.]{1,63}$', d_country)):
            return
        if not bool(re.match(r'^[a-zA-Z\(\)\s,\'\-\.]{1,63}$', a_country)):
            return
        
        serializer.save(
            traveler=self.request.user,
            departure_country=Country.objects.get(name=d_country),
            arrival_country=Country.objects.get(name=a_country))

    @detail_route(methods=['GET'])
    def generate_tasks(self, request, *args, **kwargs):
        """
        This route is called when a traveler want to regenerate every tasks
        """
        trip = self.get_object()
        trip.delete_generated_tasks()
        trip.generate_tasks()
        tasks = Task.objects.filter(trip=trip)
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)

    @detail_route(methods=['GET'])
    def tasks(self, request, *args, **kwargs):
        """
        This route is called when a traveler want to regenerate every tasks
        """
        trip = self.get_object()
        tasks = Task.objects.filter(trip=trip)
        serializer = TaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsTravelerOrIsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(traveler=user)

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrIsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


class CountryListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'name'

    serializer_class = CountrySerializer
    action_serializers = {
        'retrieve': CountrySerializer,
        'list': CountryListSerializer}
 
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]


class AirportListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsAuthenticated]

    # Overriding of a List/RetrieveMixins method
    def get_queryset(self):
        """
        Optionally restricts the returned waiting times to a given location,
        by filtering against a `location` query parameter in the URL.
        """
        country = self.request.query_params.get('country', None)
        if country is not None and bool((re.match(r'^[0-9]+$', country))):
            queryset = Airport.objects.filter(country=country)
            return queryset
        return None
    
    # Overriding of a List/RetrieveMixins method
    def list(self, request, *args, **kwargs):
        """
        If the user provided no parameters, we signal him to retry with mandatory parameters
        """
        queryset = self.filter_queryset(self.get_queryset())
        if queryset is None:
            return Response({"Warning": "Don't forget the country parameter in your url, example: /airport/?country=1"})

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
