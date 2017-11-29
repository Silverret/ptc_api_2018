"""
Script transforming a json from internet in a model json for Country table !
"""
import json

with open('raw_countries.json', 'r') as myfile:
    data = myfile.read()

raw_json = json.loads(data)
new_countries = []

for i, country in enumerate(raw_json, start=1):
    new_country = {}
    new_country["model"] = "task_factory.Country"
    new_country["pk"] = i
    new_country["fields"] = country
    new_countries.append(new_country)

with open('countries.json', 'w') as outfile:
    json.dump(new_countries, outfile, indent=4)
