import time
import requests
from django.core.management.base import BaseCommand
from ptc_api import settings
from ptc_api_back.models import Country, Vaccine, Climate


class Command(BaseCommand):
    help = 'Update the Vaccine Data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        countries_list = Country.objects.all()
        for i in range(3):
            countries_list = self.get_info(countries_list)

    def get_info(self, countries):
        refused_countries = []
        for country in countries:
            try:
                url = settings.EXTERNAL_API_URLS['tugo'] + country.code
                headers = settings.EXERNAL_API_HEADERS['tugo']
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
            except (requests.exceptions.ConnectionError):
                self.stdout.write(self.style.ERROR(
                    'Tugo API Connection error for "%s"' % country.name))
                continue
            except (requests.exceptions.Timeout):
                self.stdout.write(self.style.ERROR(
                    'Tugo API timeout error for "%s", sleeping for 10s ...' % country.name))
                refused_countries.append(country)
                time.sleep(20)
                continue
            except (requests.exceptions.HTTPError):
                self.stdout.write(self.style.ERROR(
                    'Tugo API Servor error for "%s", sleeping for 30s ...' % country.name))
                refused_countries.append(country)
                time.sleep(30)
                continue

            try:
                assert country.code == response.json()["code"]
            except (KeyError, AssertionError):
                self.stdout.write(self.style.NOTICE(
                    'Tugo API does not have information for "%s"' % country.name))
                continue

            self.get_vaccine_info(country, response)

            self.get_malaria_info(country, response)

            self.get_climate_info(country, response)

            self.get_level_alert(country, response)

            self.stdout.write(self.style.SUCCESS(
                'Successfully loaded data for "%s"' % country.name))

            time.sleep(10)

        return refused_countries

    def get_vaccine_info(self, country, response):
        try:
            vaccines_json = response.json(
            )['health']['diseasesAndVaccinesInfo']['Vaccines']
            for vaccine_json in vaccines_json:
                # try to get the vaccine in our base
                vaccine = Vaccine.objects.filter(
                    category=vaccine_json["category"])
                assert vaccine.count() <= 1

                # if no vaccine, add it
                if not bool(vaccine):
                    vaccine = Vaccine(
                        category=vaccine_json["category"],
                        description=vaccine_json["description"])
                    vaccine.save()
                else:
                    vaccine = vaccine[0]
                # add this country to this vaccine
                vaccine.countries.add(country)
        except KeyError:
            self.stdout.write(self.style.NOTICE(
                'Tugo API does not have vaccine information for "%s"' % country.name))

    def get_malaria_info(self, country, response):
        try:
            diseasesInfo = response.json()['health']['diseasesAndVaccinesInfo']
            country.malaria_presence = bool('Malaria' in diseasesInfo)
            country.save()
        except (KeyError, AssertionError):
            pass

    def get_climate_info(self, country, response):
        try:
            climate_json = response.json()["climate"]
            assert not climate_json["description"] is None
            try:
                # Get the climate if it exists
                climate = Climate.objects.get(country=country)
                climate.description = climate_json["description"]
            except Climate.DoesNotExist:
                # Else create it
                climate = Climate(
                    country=country,
                    description=climate_json["description"])
            finally:
                climate.save()
        except (KeyError, AssertionError):
            self.stdout.write(self.style.NOTICE(
                'Tugo API does not have climate information for "%s"' % country.name))

    def get_level_alert(self, country, response):
        try:
            level = response.json()['advisoryState']
            assert isinstance(level, int)
            country.advisory_state = level
            country.save()
        except (KeyError, AssertionError):
            pass
