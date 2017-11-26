from ptc_api_back.models import Trip, Segment, Task, Profile
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator



class TaskSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Task
        fields = ('url', 'id', 'trip', 'title', 'deadline', 'completed', 'comments')



class SegmentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Segment
        fields = (
            'url', 'id',
            'trip',
            'departure_airport', 'departure_country', 'departure_date_time',
            'arrival_airport', 'arrival_country', 'arrival_date_time',
            'order'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Segment.objects.all(),
                fields=('order', 'trip')
            )
        ]



class TripSerializer(serializers.HyperlinkedModelSerializer):
    traveler = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)
    tasks = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='task-detail')
    segments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='segment-detail')

    class Meta:
        model = Trip
        fields = (
            'url', 'id',
            'traveler',
            'departure_airport', 'departure_country', 'departure_date_time',
            'arrival_airport', 'arrival_country', 'arrival_date_time',
            'return_date_time',
            'segments',
            'tasks'
        )



class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    traveler = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'url', 'id','traveler', 'residence_country', 'nationalities', 'birth_date', 'visas', 'address', 'phone',
            'visited_countries', 'vaccines')



class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail', read_only=True)
    trips = serializers.HyperlinkedRelatedField(many=True, view_name='trip-detail', read_only=True)
        
    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'profile', 'trips')
