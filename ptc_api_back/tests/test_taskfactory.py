"""
API Test Case - Interaction with Task ViewSet.
"""
from datetime import datetime

from django.utils import timezone
from django.contrib.auth.models import User

from rest_framework.test import APITestCase

from ptc_api_back.task_factory import TaskFactory
from ptc_api_back.models import Country, CountryUnion

class TaskFactoryTest(APITestCase):
    """
    Tested method until now :
        - create_passport_task : 1 test
        - create_visa_task : 5 tests
        - create_malaria_tak : 2 tests
        - create_flight_needs_task : 2 tests

    Remaining method to test :
        - create_vaccine_task : 2 tests needed at least (1 done)
        - create_weather_task : ?
        - create_insurance_task : 3 tests needed (0 done)
    """

    def setUp(self):
        """
        We create a basic Database which contains :
        - 1 User
        - 1 TaskFactory
        - 2 Countries
        - 1 CountryUnion
        - 4 Trips
        - 1 Vaccine
        """
        self.tz = timezone.now().tzinfo
        self.test_user = User.objects.create_user("lauren", "secret")
        self.test_tf = TaskFactory()

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

        self.test_country_union = CountryUnion.objects.create(
            name="Schengen Area",
            t_visa_between_members=False,
            common_visa=True)
        self.test_country_union.countries.add(self.test_country1)

        self.test_trip1 = self.test_user.trips.create(
            traveler=self.test_user,
            departure_country="France",
            departure_airport="CDG",
            departure_date_time=datetime(2018, month=1, day=1, hour=18, minute=30, tzinfo=self.tz),
            arrival_country="China",
            arrival_airport="PIA",
            arrival_date_time=datetime(2018, month=1, day=2, hour=18, minute=30, tzinfo=self.tz))

        self.test_trip2 = self.test_user.trips.create(
            traveler=self.test_user,
            departure_country="France",
            departure_airport="CDG",
            departure_date_time=datetime(2018, month=1, day=1, hour=18, minute=30, tzinfo=self.tz),
            arrival_country="France",
            arrival_airport="LYA",
            arrival_date_time=datetime(2018, month=1, day=1, hour=20, minute=30, tzinfo=self.tz))

        self.test_trip3 = self.test_user.trips.create(
            traveler=self.test_user,
            departure_country="China",
            departure_airport="CAA",
            departure_date_time=datetime(2018, month=1, day=1, hour=18, minute=30, tzinfo=self.tz),
            arrival_country="China",
            arrival_airport="CXA",
            arrival_date_time=datetime(2018, month=1, day=1, hour=20, minute=30, tzinfo=self.tz))

        self.test_trip4 = self.test_user.trips.create(
            traveler=self.test_user,
            departure_country="China",
            departure_airport="CAA",
            departure_date_time=datetime(2018, month=1, day=1, hour=18, minute=30, tzinfo=self.tz),
            arrival_country="France",
            arrival_airport="CDG",
            arrival_date_time=datetime(2018, month=1, day=2, hour=7, minute=30, tzinfo=self.tz))

        self.test_country2.vaccines.create(
            category="Routine Vaccines",
            description="Routine Vaccines"
        )


    def test_create_passport_task0(self):
        """
        Ensure the TaskFactory generate the correct passport task.
        """
        self.test_tf.trip = self.test_trip1

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_passport_task()

        self.assertEqual(len(self.test_tf.tasks), 1)

    def test_create_visa_task0(self):
        """
        Ensure the TaskFactory generate the correct visa task
        If we don't have departure country nor arrival coutry.
        """
        self.test_tf.trip = self.test_trip1

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_visa_task()

        self.assertEqual(len(self.test_tf.tasks), 1)

        visa_task = self.test_tf.tasks[0]
        self.assertEqual(
            visa_task.title,
            "Visa may be needed")

    def test_create_visa_task1(self):
        """
        Ensure the TaskFactory generate the correct visa task for trip1.
        """
        self.test_tf.trip = self.test_trip1
        self.test_tf.d_country = self.test_country1
        self.test_tf.a_country = self.test_country2

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_visa_task()

        self.assertEqual(len(self.test_tf.tasks), 1)

        visa_task = self.test_tf.tasks[0]
        self.assertEqual(
            visa_task.title,
            self.test_country2.name + "'s Visa needed")

    def test_create_visa_task2(self):
        """
        Ensure the TaskFactory generate the correct visa task for trip2.
        """
        self.test_tf.trip = self.test_trip2
        self.test_tf.d_country = self.test_country1
        self.test_tf.a_country = self.test_country1

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_visa_task()

        self.assertEqual(len(self.test_tf.tasks), 1)

        visa_task = self.test_tf.tasks[0]
        self.assertEqual(visa_task.title, "No Visa needed")

    def test_create_visa_task3(self):
        """
        Ensure the TaskFactory generate the correct visa task for trip3.
        """
        self.test_tf.trip = self.test_trip3
        self.test_tf.d_country = self.test_country2
        self.test_tf.a_country = self.test_country2

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_visa_task()

        self.assertEqual(len(self.test_tf.tasks), 1)

        visa_task = self.test_tf.tasks[0]
        self.assertEqual(visa_task.title, "No Visa needed")

    def test_create_visa_task4(self):
        """
        Ensure the TaskFactory generate the correct visa task for trip4.
        """
        self.test_tf.trip = self.test_trip3
        self.test_tf.d_country = self.test_country2
        self.test_tf.a_country = self.test_country1

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_visa_task()

        self.assertEqual(len(self.test_tf.tasks), 1)

        visa_task = self.test_tf.tasks[0]
        self.assertEqual(visa_task.title, "A Visa is needed")

    def test_create_malaria_task0(self):
        """
        Ensure the TaskFactory generate the correct malaria task for trip1.
        """
        self.test_tf.trip = self.test_trip1
        self.test_tf.d_country = self.test_country1
        self.test_tf.a_country = self.test_country2

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_malaria_task()

        self.assertEqual(len(self.test_tf.tasks), 1)

    def test_create_malaria_task1(self):
        """
        Ensure the TaskFactory generate the correct malaria task for trip3.
        """
        self.test_tf.trip = self.test_trip3
        self.test_tf.d_country = self.test_country2
        self.test_tf.a_country = self.test_country1

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_malaria_task()

        self.assertEqual(len(self.test_tf.tasks), 0)

    def test_create_flight_needs_task0(self):
        """
        Ensure the TaskFactory generate the correct flight needs task for trip1.
        """
        self.test_tf.trip = self.test_trip1
        self.test_tf.d_country = self.test_country1
        self.test_tf.a_country = self.test_country2

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_flight_needs_task()

        self.assertEqual(len(self.test_tf.tasks), 1)
        
        tested_task = self.test_tf.tasks[0]
        self.assertEqual(
            tested_task.comments,
            "Take your earplugs and your sleep mask for your flight")

    def test_create_flight_needs_task1(self):
        """
        Ensure the TaskFactory generate the correct flight needs task for trip2.
        """
        self.test_tf.trip = self.test_trip2
        self.test_tf.d_country = self.test_country1
        self.test_tf.a_country = self.test_country1

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_flight_needs_task()

        self.assertEqual(len(self.test_tf.tasks), 1)
        
        tested_task = self.test_tf.tasks[0]
        self.assertEqual(
            tested_task.comments,
            "Take some food and some drinks for your flight")

    def test_create_vaccines_task0(self):
        """
        Ensure the TaskFactory generate the correct vaccines task for trip1.
        """
        self.test_tf.trip = self.test_trip1
        self.test_tf.d_country = self.test_country1
        self.test_tf.a_country = self.test_country2

        self.assertEqual(len(self.test_tf.tasks), 0)

        self.test_tf.create_vaccines_task()

        self.assertEqual(len(self.test_tf.tasks), 1)
        
        tested_task = self.test_tf.tasks[0]
        self.assertEqual(
            tested_task.comments,
            "\t- Routine Vaccines")
