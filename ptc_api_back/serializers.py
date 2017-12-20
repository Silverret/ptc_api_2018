from ptc_api_back.models import Trip, Segment, Task, Profile
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator



class TaskSerializer(serializers.HyperlinkedModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only = ('id', 'auto')



class SegmentSerializer(serializers.HyperlinkedModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Segment
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Segment.objects.all(),
                fields=('order', 'trip')
            )
        ]


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    traveler = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(many=False, view_name='profile-detail', read_only=True)
    trips = serializers.HyperlinkedRelatedField(many=True, view_name='trip-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'profile', 'trips')


class TripSerializer(serializers.HyperlinkedModelSerializer):
    traveler = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)
    segments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='segment-detail')

    class Meta:
        model = Trip
        fields = (
            'id',
            'traveler',
            'departure_airport', 'departure_country', 'departure_date_time',
            'arrival_airport', 'arrival_country', 'arrival_date_time',
            'return_date_time',
            'segments'
        )
