"""
Viewsets of the API are defined here
"""
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets, mixins
from rest_framework.decorators import api_view, permission_classes, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from ptc_api_back.models import Trip, Segment, Task, Profile
from ptc_api_back.serializers import UserSerializer, ProfileSerializer, TripSerializer, SegmentSerializer, TaskSerializer
from ptc_api_back.permissions import IsOwnerOrReadOnly, IsOwnerOfTheTripOrReadOnly, IsUserOrReadOnly
from task_factory.models import Country
from task_factory.serializers import CountrySerializer


@api_view(['GET'])
@permission_classes((permissions.AllowAny, ))
def api_root(request, format=None):
    """
    Default route, presents every viewsets available
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'profiles': reverse('profile-list', request=request, format=format),
        'trips': reverse('trip-list', request=request, format=format),
        'segments': reverse('segment-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format)
    })



class TaskViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOfTheTripOrReadOnly]

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
    permission_classes = [IsOwnerOfTheTripOrReadOnly]


    def perform_create(self, serializer):
        """
        We try to get the trip specified in the initial data
        """
        try:
            cor_trip = Trip.objects.get(id=serializer.initial_data['trip'].split("/")[-2])
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
    permission_classes = [IsOwnerOrReadOnly]
    """
    permission_classes has to be improved to disable anonymousUser to
    GET the route "generate_tasks"
    """

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

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)



class ProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(traveler=self.request.user)



class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly]

class CountryListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    