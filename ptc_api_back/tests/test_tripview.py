from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework.test import RequestsClient
from rest_framework import status
from rest_framework.authtoken.models import Token

class TripTest(APITestCase):
    def setUp(self):
        """
        We create a basic Database which contains :
        - 1 User
        """
        self.test_user = User.objects.create_user("lauren", "secret")
        self.tz = timezone.now().tzinfo

    def test_post0(self):
        """
        Ensure a User can POST a Trip.
        """
        token = Token.objects.get(user__username='lauren')
        client = RequestsClient()
        client.headers.update({"Authorization": f'Token {token.key}'})

        old_trips_count = self.test_user.trips.count()
        response = client.post(
            "http://localhost:8000/trips/",
            json={
                "departure_airport": "CTU",
                "departure_country": "China",
                "departure_date_time": "2017-12-06T18:00:00Z",
                "arrival_airport": "IAT",
                "arrival_country": "Spain",
                "arrival_date_time": "2017-12-07T09:30:00Z",
                "segments": []
            },
            headers={"Content-Type": 'application/json'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.test_user.trips.count(),
            old_trips_count+1)

    def test_delete0(self):
        """
        Ensure a User can DELETE a Trip.
        """
        token = Token.objects.get(user__username='lauren')
        client = RequestsClient()
        client.headers.update({"Authorization": f'Token {token.key}'})

        self.test_user.trips.create(
            departure_airport="CTU",
            departure_country="China",
            departure_date_time=datetime(2018, month=1, day=1, hour=12, minute=0, tzinfo=self.tz),
            arrival_airport="IAT",
            arrival_country="Spain",
            arrival_date_time=datetime(2018, month=1, day=1, hour=15, minute=0, tzinfo=self.tz),
        )

        old_trips_count = self.test_user.trips.count()

        response = client.delete(
            "http://localhost:8000/trips/1",
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.test_user.trips.count(),
            old_trips_count-1)
