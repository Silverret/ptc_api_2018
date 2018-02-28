import json

from django.core.management.base import BaseCommand

from ptc_api_back.models import Country


class Command(BaseCommand):
    help = 'Import the Airport Data.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        csv = open('ptc_api_back/fixtures/AIRPORTS_LIST.csv', 'r')
        jsonfile = open('ptc_api_back/fixtures/airport.json', 'w')

        rows = csv.read().split('\n')
        airports = list()
        pk = 1
        for row in rows:
            elems = row.split(';')
            if len(elems) < 6:
                continue
            if elems[5] != 'Y':
                continue
            if not Country.objects.filter(code=elems[3]):
                continue
            fields = {}
            fields['code'] = elems[0]
            fields['name'] = elems[1] if elems[1] != "" else None
            fields['city'] = str.title(elems[2])
            fields['country'] = Country.objects.get(code=elems[3]).id
            airport = {}
            airport['model'] = 'ptc_api_back.airport'
            airport['pk'] = pk
            pk += 1
            airport['fields'] = fields
            airports.append(airport)

        json.dump(airports, jsonfile)

        jsonfile.close()
        csv.close()

