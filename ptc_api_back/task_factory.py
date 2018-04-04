"""
This is the magic !

In this module, we generate the specific required tasks for each trip !
"""
from datetime import timedelta
from ptc_api_back.models import Country, Climate, TaskCategory


class TaskFactory:
    """
    Factory class designed to help create various tasks.
    """

    def __init__(self, trip):
        self.trip = trip
        self.d_country = self.trip.departure_country
        self.a_country = self.trip.arrival_country
        self.tasks = []

    def create_tasks(self):
        """
        Call the task_factory method to create the differents tasks.
        """
        self.create_passport_task()

        self.create_visa_task()

        self.create_vaccines_task()
        self.create_malaria_task()

        self.create_weather_task()
        self.create_flight_needs_task()
        self.create_banking_task()

        self.create_insurance_task()

        self.create_systematic_tasks()  # 3 tasks

        if self.trip.return_date_time is None or\
            self.trip.return_date_time - self.trip.arrival_date_time > timedelta(days=14):

            self.create_long_travel_task()

        for task in self.tasks:
            task.auto = True

        return self.tasks

    def create_passport_task(self):
        self.tasks.append(self.trip.tasks.create(
            title="Check Passport Validity Date",
            comments="Most of the time, your passport has to be valid " +\
            "at least three months after your departure.",
            category=TaskCategory.objects.get(name="Paperwork"),
            deadline=self.trip.departure_date_time - timedelta(days=2*30)
        ))

    def create_visa_task(self):

        if self.d_country is self.a_country:
            self.tasks.append(self.trip.tasks.create(
                title="No Visa is needed for this country.",
                category=TaskCategory.objects.get(name="Paperwork"),
                deadline=self.trip.departure_date_time - timedelta(days=1*30)
            ))
            return

        common_unions = set()
        for union in self.d_country.countryunion_set.all():
            if bool(union.countries.filter(id=self.a_country.id)):
                common_unions.add(union)

        if bool(common_unions):
            for union in common_unions:
                if not union.t_visa_between_members:
                    self.tasks.append(self.trip.tasks.create(
                        title="No Visa is needed for this country.",
                        category=TaskCategory.objects.get(name="Paperwork"),
                        deadline=self.trip.departure_date_time - timedelta(days=1*30)
                    ))
                    return

        common_visa_unions = self.a_country.countryunion_set.filter(common_visa=True)
        if common_visa_unions:
            str_visa_list = ""
            for union in common_visa_unions:
                str_visa_list += "\n\t- "+union.name+""'s Visa'
            self.tasks.append(self.trip.tasks.create(
                title="A Visa is needed",
                comments="You have the choice between :" + str_visa_list,
                category=TaskCategory.objects.get(name="Paperwork"),
                deadline=self.trip.departure_date_time - timedelta(days=1*30)
            ))
            return

        self.tasks.append(self.trip.tasks.create(
            title=self.a_country.name + "'s Visa needed",
            comments="Contact the Ambassy of the destination country.",
            category=TaskCategory.objects.get(name="Paperwork"),
            deadline=self.trip.departure_date_time - timedelta(days=1*30)
        ))

    def create_vaccines_task(self):
        """
        #TODO
        """
        comments = ""
        vaccines = self.a_country.vaccines.all()
        if bool(vaccines):
            comments = ""
            for vaccine in vaccines:
                comments += vaccine.category+" - "
            self.tasks.append(self.trip.tasks.create(
                title="Check vaccines",
                comments=comments[:-3],
                category=TaskCategory.objects.get(name="Health"),
                deadline=self.trip.departure_date_time - timedelta(days=45)
            ))
            return

        self.tasks.append(self.trip.tasks.create(
            title="Check vaccines for " + self.a_country.name,
            comments="Both required and advised vaccines !",
            category=TaskCategory.objects.get(name="Health"),
            deadline=self.trip.departure_date_time - timedelta(days=45)
        ))

    def create_malaria_task(self):
        """
        Check if country has malaria presence.
        """
        if not self.a_country is self.d_country and self.a_country.malaria_presence:
            self.tasks.append(self.trip.tasks.create(
                title="Protection against mosquitoes",
                comments="Insect repellent, insecticide-treated bednet and pre-treating clothing",
                category=TaskCategory.objects.get(name="Health"),
                deadline=self.trip.departure_date_time - timedelta(days=3)
            ))

    def create_weather_task(self):
        """
        Climate information comes from Tugo.
        They may be frightening ;-)
        """
        try:
            climate = Climate.objects.get(country=self.a_country)
            self.tasks.append(self.trip.tasks.create(
                title=f"Check climate in {self.a_country.name}",
                comments=climate.description,
                category=TaskCategory.objects.get(name="Others"),
                deadline=self.trip.departure_date_time - timedelta(days=3)
            ))
        except (Climate.DoesNotExist, Country.DoesNotExist):
            self.tasks.append(self.trip.tasks.create(
                title="Check meteo",
                comments="Check weather conditions in " + self.a_country.name +\
                " and prepare appropriate clothing",
                category=TaskCategory.objects.get(name="Others"),
                deadline=self.trip.departure_date_time - timedelta(days=3)
            ))

    def create_flight_needs_task(self):
        """
        Create a task "take some food/drinks/books/earplugs" if the flight is too long.
        """
        duration = self.trip.arrival_date_time - self.trip.departure_date_time
        if duration > timedelta(hours=2):
            self.tasks.append(self.trip.tasks.create(
                title="Flight Must Have !",
                comments="It's a long flight ! Don't forget your earplugs and your sleep mask.",
                category=TaskCategory.objects.get(name="Others"),
                deadline=self.trip.departure_date_time - timedelta(days=1)
            ))
        else:
            self.tasks.append(self.trip.tasks.create(
                title="Flight Must Have !",
                comments="Take some food and some drinks for your flight",
                category=TaskCategory.objects.get(name="Others"),
                deadline=self.trip.departure_date_time - timedelta(days=1)
            ))

    def create_banking_task(self):
        self.tasks.append(self.trip.tasks.create(
            title="Check your banking fees",
            comments="Contact your bank account manager " +\
            "to ask him about the amount of banking fees you will have to pay " +\
            "when you use your credit card at the destination.",
            category=TaskCategory.objects.get(name="Paperwork"),
            deadline=self.trip.departure_date_time - timedelta(days=10)
        ))

    def create_insurance_task(self):
        level = self.a_country.advisory_state
        if not level is None:
            self.tasks.append(self.trip.tasks.create(
                title="Check repatriation insurance",
                comments="It seems to be recommended for this country !" if level > 0\
                    else "Not absolutely required but if you need this to relax, go on :-)",
                category=TaskCategory.objects.get(name="Paperwork"),
                deadline=self.trip.departure_date_time - timedelta(days=14)
            ))
        else:
            self.tasks.append(self.trip.tasks.create(
                title="Check required insurance",
                comments="We got no information for your country, sorry !",
                category=TaskCategory.objects.get(name="Paperwork"),
                deadline=self.trip.departure_date_time - timedelta(days=14)
            ))

    def create_systematic_tasks(self):
        self.tasks.append(self.trip.tasks.create(
            title="Check cabin baggage dimensions",
            comments="Check what are the maximum dimensions of baggages allowed on board.",
            category=TaskCategory.objects.get(name="Others"),
            deadline=self.trip.departure_date_time - timedelta(days=5)
        ))
        self.tasks.append(self.trip.tasks.create(
            title="Labels on your baggages",
            comments="It really helps if your baggages are lost during the flight !",
            category=TaskCategory.objects.get(name="Others"),
            deadline=self.trip.departure_date_time - timedelta(days=1)
        ))
        self.tasks.append(self.trip.tasks.create(
            title="Make copies of your pappers.",
            comments="Make sure you have duplicates of your visa and your passport. " +\
            "Save them on your smartphone or have them retrievable from the internet.",
            category=TaskCategory.objects.get(name="Others"),
            deadline=self.trip.departure_date_time - timedelta(days=2)
        ))

    def create_long_travel_task(self):
        """
        #TODO
        """
        self.tasks.append(self.trip.tasks.create(
            title="Do you have a pet?",
            comments="Don't forget to make sure it is looked after.",
            category=TaskCategory.objects.get(name="Others"),
        ))
