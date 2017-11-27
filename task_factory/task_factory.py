"""
This is the magic !

In this module, we generate the specific required tasks for each trip !
"""
from datetime import timedelta
import requests
from ptc_api import settings
from task_factory.models import Country



class TaskFactory:
    """
    Factory class designed to help create various tasks.
    """
    def __init__(self, **kwargs):
        self.trip = kwargs['trip'] if 'trip' in kwargs else None

    def create_tasks(self):
        """
        Call the task_factory method to create the differents tasks.
        """
        tasks = {
            self.create_weather_task(),
            self.create_flight_needs_task(),
        }
        for task in self.create_vaccinces_tasks():
            tasks.add(task)

        return tasks

    def create_weather_task(self):
        """
        Create a task "go check weather conditions in your destination country".
        """
        return self.trip.tasks.create(
            title="Check weather conditions in "+
            self.trip.arrival_country + " and prepare appropriate clothing"
        )

    def create_flight_needs_task(self):
        """
        Create a task "take some food/drinks/books/earplugs" if the flight is too long.
        """
        duration = self.trip.arrival_date_time - self.trip.departure_date_time
        if duration > timedelta(hours=2):
            return self.trip.tasks.create(
                title="Take your earplugs and your sleep mask for your flight"
            )
        else:
            return self.trip.tasks.create(
                title="Take some food and some drinks for your flight"
            )

    def create_vaccinces_tasks(self):
        """
        Call the API of TuGo
        https://api.tugo.com/v1/travelsafe/countries/[CodeCountry]
        headers must contain : "X-Auth-API-Key":"jttuskf9wetdbzspvtt6kagb"
        """
        tasks = set()
        try:
            country = Country.objects.filter(name=self.trip.arrival_country)[0]
            url = settings.EXTERNAL_API_URLS['tugo']+country.code
            headers = settings.EXERNAL_API_HEADERS['tugo']
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                for vaccine in response.json()['health']['diseasesAndVaccinesInfo']['Vaccines']:
                    tasks.add(self.trip.tasks.create(
                        title="Vaccine : " + vaccine['category'],
                        comments=vaccine['description'],
                        deadline=self.trip.departure_date_time - timedelta(days=45)
                    ))
        except (KeyError, requests.exceptions.ConnectionError, Country.DoesNotExist):
            tasks.add(self.trip.tasks.create(
                title="Check required and advised vaccines for " + self.trip.arrival_country,
                deadline=self.trip.departure_date_time - timedelta(days=45)
            ))
        finally:
            return tasks
