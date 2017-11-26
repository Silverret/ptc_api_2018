"""
This is the magic !

In this module, we generate the specific required tasks for each trip !
"""
from datetime import timedelta
from ptc_api_back.models import Task


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
            'WEATHER': self.create_weather_task(),
            'FLIGHT_NEEDS' : self.create_flight_needs_task(),
        }
        return tasks

    def create_weather_task(self):
        """
        Create a task "go check weather conditions in your destination country".
        """
        return Task(
            title="Check weather conditions in "+
            self.trip.arrival_country + " and prepare appropriate clothing"
        )

    def create_flight_needs_task(self):
        """
        Create a task "take some food/drinks/books/earplugs" if the flight is too long.
        """
        duration = self.trip.arrival_date_time - self.trip.departure_date_time
        if duration > timedelta(hours=2):
            return Task(
                title="Take your earplugs and your sleep mask for your flight"
            )
        else:
            return Task(
                title="Take some food and some drinks for your flight"
            )
