from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from ptc_api_back.models import Trip, Task
from task_factory.models import Country

class TripTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user('testuser', 'test@example.com', 'testpassword')

        Country.objects.create(
            name="China",
            code="CN"
        )
        Country.objects.create(
            name="Spain",
            code="ES"
        )
        # URL for creating an trip.
        self.create_url = reverse('trip-list')
        self.destroy_url = reverse('trip-detail', args=(1,))

    def test_create_trip(self):
        """
        Ensure we can create a new trip and the auto tasks are created with it.
        When the two countries are valid.
        """
        data = {
            "departure_airport": "CTU",
            "departure_country": "China",
            "departure_date_time": "2017-12-06T18:00:00Z",
            "arrival_airport": "IAT",
            "arrival_country": "Spain",
            "arrival_date_time": "2017-12-07T09:30:00Z",
            "segments": []
        }

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.create_url, data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(Trip.objects.count(), 1)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertGreater(Task.objects.filter(trip_id=1).count(), 0)

    def test_create_trip_no_valid_country(self):
        """
        Ensure we can create a new trip and the auto tasks are created with it.
        When none country is valid.
        """
        data = {
            "departure_airport": "CTU",
            "departure_country": "Chinazz",
            "departure_date_time": "2017-12-06T18:00:00Z",
            "arrival_airport": "IAT",
            "arrival_country": "Spainzz",
            "arrival_date_time": "2017-12-07T09:30:00Z",
            "segments": []
        }

        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.create_url, data, format='json')

        # We want to make sure we have two users in the database..
        self.assertEqual(Trip.objects.count(), 1)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertGreater(Task.objects.filter(trip_id=1).count(), 0)

    def test_destroy_trip(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.delete(self.destroy_url)

        # We want to make sure we have two users in the database..
        self.assertEqual(Trip.objects.count(), 0)
        
