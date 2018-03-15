"""
API Test Case - Interaction with Task ViewSet.
"""
from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.test import RequestsClient
from rest_framework import status
from rest_framework.authtoken.models import Token

from ptc_api_back.models import Trip, Country


class TasksVieuTest(APITestCase):

    def setUp(self):
        """
        We create a basic Database which contains :
        - 1 User
        - 1 Trip
        """
        self.test_user = User.objects.create_user("lauren", "secret")
        self.tz = timezone.now().tzinfo
        
        self.test_country1 = Country.objects.create(
            name="France",
            code="FR",
            advisory_state=1,
            malaria_presence=False)
        self.test_country2 = Country.objects.create(
            name="China",
            code="CN",
            advisory_state=1,
            malaria_presence=True)

        self.test_trip = Trip.objects.create(
            traveler=self.test_user,
            departure_country=self.test_country1,
            departure_airport="CDG",
            departure_date_time=datetime(2018, month=1, day=1, hour=18, minute=30, tzinfo=self.tz),
            arrival_country=self.test_country2,
            arrival_airport="PIA",
            arrival_date_time=datetime(2018, month=1, day=18, hour=18, minute=30, tzinfo=self.tz))

    def test_post0(self):
        """
        Ensure a User can POST a custom Task on one of its trips.
        """
        token = Token.objects.get(user__username='lauren')
        client = RequestsClient()
        client.headers.update({"Authorization": f'Token {token.key}'})

        trip_id = self.test_trip.id
        old_tasks_count = self.test_trip.tasks.count()
        response = client.post(
            'http://127.0.0.1:8000/tasks/',
            json={
                "trip": trip_id,
                "title": "Test",
                "deadline": None,
                "completed": True,
                "comments": "ceci est un test",
                "auto": True,
                "isVisible": True
            },
            headers={"Content-Type": 'application/json'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.test_trip.tasks.count(),
            old_tasks_count+1)

    def test_post1(self):
        """
        Ensure an Anonymous User can NOT POST a custom Task .
        """
        client = RequestsClient()

        trip_id = self.test_trip.id
        old_tasks_count = self.test_trip.tasks.count()
        response = client.post(
            'http://127.0.0.1:8000/tasks/',
            json={
                "trip": trip_id,
                "title": "Test",
                "deadline": None,
                "completed": True,
                "comments": "ceci est un test",
                "auto": True,
                "isVisible": True
            },
            headers={"Content-Type": 'application/json'})

        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            self.test_trip.tasks.count(),
            old_tasks_count)

    def test_post2(self):
        """
        Ensure an User can NOT POST a custom Task on a trip he doesn't own.
        """
        test_user2 = User.objects.create_user("loic", "secret")
        token = Token.objects.get(user__username='loic')
        client = RequestsClient()
        client.headers.update({"Authorization": f'Token {token.key}'})

        trip_id = self.test_trip.id
        old_tasks_count = self.test_trip.tasks.count()
        response = client.post(
            'http://127.0.0.1:8000/tasks/',
            json={
                "trip": trip_id,
                "title": "Test",
                "deadline": None,
                "completed": True,
                "comments": "ceci est un test",
                "auto": True,
                "isVisible": True
            },
            headers={"Content-Type": 'application/json'})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            self.test_trip.tasks.count(),
            old_tasks_count)
