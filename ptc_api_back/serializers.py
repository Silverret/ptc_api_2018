from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from django.contrib.auth.models import User

from ptc_api_back.models import Trip, Segment, Task, Profile, Country, Airport


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('name', 'code', 'image')
        read_only_fields = ('id', 'name', 'code')


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
                fields=('order', 'trip'))
        ]


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    traveler = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(
        many=False, view_name='profile-detail', read_only=True)
    trips = serializers.HyperlinkedRelatedField(
        many=True, view_name='trip-detail', read_only=True)
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], password=validated_data['password'])
        return user

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'password', 'profile', 'trips')


class TripSerializer(serializers.HyperlinkedModelSerializer):
    traveler = serializers.HyperlinkedRelatedField(
        many=False, view_name='user-detail', read_only=True)
    segments = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='segment-detail')
    departure_country = CountrySerializer(many=False, read_only=True)
    arrival_country = CountrySerializer(many=False, read_only=True)

    class Meta:
        model = Trip
        fields = (
            'id', 'traveler',
            'departure_airport', 'departure_country', 'departure_date_time',
            'arrival_airport', 'arrival_country', 'arrival_date_time',
            'return_date_time','segments')

class AirportSerializer(serializers.HyperlinkedModelSerializer):
    country = serializers.HyperlinkedRelatedField(
        many=False, read_only=True, view_name='country-detail')

    class Meta:
        model = Airport
        fields = ('code', 'name', 'city', 'country')
        read_only_fields = ('id', 'code', 'name', 'city', 'country')
