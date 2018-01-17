"""
API Test Case - Interaction with Task ViewSet.
"""
from datetime import datetime

# from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.test import RequestsClient
from rest_framework.authtoken.models import Token

from ptc_api_back.models import Trip


class TasksVieuTest(APITestCase):

    def setUp(self):
        """
        We create a basic Database which contains :
        - 1 User
        - 1 Trip
        """
        self.test_user = User.objects.create_user("lauren", "secret")

        self.tz = timezone.now().tzinfo

        self.test_trip = Trip.objects.create(
            traveler=self.test_user,
            departure_country="France",
            departure_airport="CDG",
            departure_date_time=datetime(2018, month=1, day=1, hour=18, minute=30, tzinfo=self.tz),
            arrival_country="China",
            arrival_airport="PIA",
            arrival_date_time=datetime(2018, month=1, day=18, hour=18, minute=30, tzinfo=self.tz))

    def test_post(self):
        token = Token.objects.get(user__username='lauren')
        client = RequestsClient()
        client.headers.update({"Authorization": f'Token {token.key}'})

        trip_id = self.test_trip.id
        response = client.post(
            'http://localhost:8000/tasks/',
            json={
                "trip": f"{trip_id}",
                "title": "Test",
                "deadline": None,
                "completed": True,
                "comments": "ceci est un test",
                "auto": True,
                "isVisible": True
            },
            headers={"Content-Type": 'application/json'})

        self.assertEqual(response.status_code, 201)
