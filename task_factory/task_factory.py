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
        self.tugo_response = None
        self.a_country = None
        self.d_country = None

    def create_tasks(self):
        """
        Call the task_factory method to create the differents tasks.
        """
        try:
            self.a_country = Country.objects.filter(name=self.trip.arrival_country)[0]
            self.d_country = Country.objects.filter(name=self.trip.departure_country)[0]
            url = settings.EXTERNAL_API_URLS['tugo']+self.a_country.code
            headers = settings.EXERNAL_API_HEADERS['tugo']
            self.tugo_response = requests.get(url, headers=headers)
        except (requests.exceptions.ConnectionError):
            pass
        except Country.DoesNotExist:
            pass

        tasks = []
        tasks.append(self.create_passport_task()),
        tasks += self.create_visa_task(),
        tasks += [self.create_vaccines_task(),
            self.create_weather_task(),
            self.create_flight_needs_task(),
            self.create_banking_task(),
            self.create_insurance_task()]

        tasks += self.create_trip_needs_tasks() #1-3 tasks
        tasks += self.create_systematic_tasks() #3 tasks

        if self.trip.return_date_time is None or self.trip.return_date_time - self.trip.arrival_date_time > timedelta(days=14):
            tasks.append(self.create_long_travel_task())

        for task in tasks:
            task.auto = True

        return tasks

    def create_passport_task(self):
        """
        Voir Donnée non formatée de l'année dernière IATA github !
        """
        return self.trip.tasks.create(
            title="Check Passport Validity Date",
            comments="Most of the time, your passport has to be valid at least for the three months following your departure.")

    def create_visa_task(self):
        if self.d_country is None or self.a_country is None:
            return [self.trip.tasks.create(
                title="Visa may be needed.",
                comments="We don't have your country in our base, retry with its name in English please."
                )]
        
        d_country = self.d_country
        a_country = self.a_country

        common_unions = set()
        for union in d_country.countryunion_set.all():
            if bool(union.countries.filter(id=a_country.id)):
                common_unions.add(union)

        if len(common_unions) > 0:
            for union in common_unions:
                if not union.t_visa_between_members:
                    return [self.trip.tasks.create(title="No Visa Needed")]

        tasks = []
        for union in a_country.countryunion_set.all():
            if union.common_visa:
                tasks.append(self.trip.tasks.create(title=union.name + "Visa or"))

        tasks.append(self.trip.tasks.create(
            title=a_country.name + "'s Visa Needed",
            comments="Contact the Ambassy of your destination country."))
        
        return tasks

    def create_vaccines_task(self):
        """
        Call the API of TuGo
        https://api.tugo.com/v1/travelsafe/countries/[CodeCountry]
        headers must contain : "X-Auth-API-Key":"jttuskf9wetdbzspvtt6kagb"
        """
        comments = ""
        try:
            if self.tugo_response.status_code == 200:
                for vaccine in self.tugo_response.json()['health']['diseasesAndVaccinesInfo']['Vaccines']:
                    comments += vaccine['category'] + "\n"
                return self.trip.tasks.create(
                    title="Check your vaccines",
                    comments=comments,
                    deadline=self.trip.departure_date_time - timedelta(days=45))

        except (KeyError):
            return self.trip.tasks.create(
                title="Check vaccines for " + self.trip.arrival_country,
                comments="Both required and advised vaccines !",
                deadline=self.trip.departure_date_time - timedelta(days=45))

    def create_weather_task(self):
        """
        Create a task "go check weather conditions in your destination country".
        https://datahelpdesk.worldbank.org/knowledgebase/articles/902061-climate-data-api
        """
        return self.trip.tasks.create(
            title="Check meteo",
            comments="Check weather conditions in " + self.trip.arrival_country + " and prepare appropriate clothing"
        )

    def create_flight_needs_task(self):
        """
        Create a task "take some food/drinks/books/earplugs" if the flight is too long.
        """
        duration = self.trip.arrival_date_time - self.trip.departure_date_time
        if duration > timedelta(hours=2):
            return self.trip.tasks.create(
                title="Flight Must Have !",
                comments="Take your earplugs and your sleep mask for your flight"
            )
        else:
            return self.trip.tasks.create(
                title="Flight Must Have !",
                comments="Take some food and some drinks for your flight")

    def create_banking_task(self):
        return self.trip.tasks.create(
            title="Check your banking fees",
            comments="You should contact your bank account manager to ask the amount of banking fees you will have to pay when you will pay with your card or when you will use a cash machine.")

    def create_insurance_task(self):
        if self.tugo_response.status_code == 200:
            level = self.tugo_response.json()['advisoryState']
            return self.trip.tasks.create(
                title="Check rapatriation insurance",
                comments="It seems to be recommended for this country !" if level > 0 else "Not really required but if you need this to relax yourself, go on :-)")
        return self.trip.tasks.create(
            title="Check required insurance",
            comments="We got no information for your country, sorry !")

    def create_trip_needs_tasks(self):
        return []

    def create_systematic_tasks(self):
        tasks = []
        tasks.append(self.trip.tasks.create(
            title="Check cabin baggage dimensions",
            comments="Ask your company website which size your cabin baggage can be."
        ))
        tasks.append(self.trip.tasks.create(
            title="Labels on your baggages",
            comments="It really helps if your baggages are lost during the flight !"
        ))
        tasks.append(self.trip.tasks.create(
            title="Make copies of your pappers.",
            comments="Put one copy of your passport, your visa and your flight ticket in each luggage. Copy them on your smartphone and have them on the internet."
        ))
        return(tasks)

    def create_long_travel_task(self):
        return self.trip.tasks.create(
            title="Long travel To-Do",
            comments="")
