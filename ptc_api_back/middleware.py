"""
This middleware was created by the 2016-2017 team.
It is able to treat some complex POST request containing Amadeus Trip Object.
It is not used in the current app. It is not declared in the MIDDLEWARES settings.
"""
import json
from datetime import datetime

class TripProcessingMiddleware(object):
    """
    Middleware to intercept POST requests made to create a trip
    and make them more suitable to our API.
    Especially, filter the fields in the incoming data that need to be renamed to suit our model,
    and handle "segments" in a different request.
    """
    def process_request(self, request):
        if request.path_info == '/trips/' and request.method == 'POST':
            raw_request_json = request.body
            clean_body = json.loads(raw_request_json.decode("utf-8"))
            final_data = {}

            # Process or searches all required data
            if "departure_airport" in clean_body.keys():
                final_data['departure_airport'] = clean_body['departure_airport']
            elif "fromLocation" in clean_body.keys() and "name" in clean_body['fromLocation'].keys():
                final_data['departure_airport'] = clean_body['fromLocation']['name']

            if "departure_country" in clean_body.keys():
                final_data['departure_country'] = clean_body['departure_country']
            elif "fromLocation" in clean_body.keys() and "countryName" in clean_body['fromLocation'].keys():
                final_data['departure_country'] = clean_body['fromLocation']['countryName']

            if "departure_date_time" in clean_body.keys():
                final_data['departure_date_time'] = clean_body['departure_date_time']
            elif "startDate" in clean_body.keys() and "utcTimestampMillis" in clean_body['startDate'].keys():
                final_data['departure_date_time'] = datetime.utcfromtimestamp(
                    clean_body['startDate']['utcTimestampMillis']/1000)

            if "arrival_airport" in clean_body.keys():
                final_data['arrival_airport'] = clean_body['arrival_airport']
            elif "toLocation" in clean_body.keys() and "name" in clean_body['toLocation'].keys():
                final_data['arrival_airport'] = clean_body['toLocation']['name']

            if "arrival_country" in clean_body.keys():
                final_data['arrival_country'] = clean_body['arrival_country']
            elif "toLocation" in clean_body.keys() and "countryName" in clean_body['toLocation'].keys():
                final_data['arrival_country'] = clean_body['toLocation']['countryName']

            # The endDate in the JSON file is the end of the trip, not the arrival time!
            # It can be the arrival time if no return, else we have to check the segments.
            if "arrival_date_time" in clean_body.keys():
                final_data['arrival_date_time'] = clean_body['arrival_date_time']
            elif "tripDetails" in clean_body.keys():
                final_data['arrival_date_time'], final_data['return_date_time'] = get_arrival_and_return_from_segment(
                    clean_body['tripDetails']['segments'],
                    final_data['departure_airport'],
                    final_data['arrival_airport'])

            if "return_date_time" in clean_body.keys():
                final_data['return_date_time'] = clean_body['return_date_time']

            if "segments" in clean_body.keys():
                final_data['segments'] = clean_body["segments"]
            elif "tripDetails" in clean_body.keys():
                final_data['segments'] = format_segments(clean_body['tripDetails']['segments'])

            if "bookingFirstName" in clean_body.keys() and "bookingLastName" in clean_body.keys():
                final_data['first_name'] = clean_body["bookingFirstName"]
                final_data['last_name'] = clean_body["bookingLastName"]
            else:
                final_data['first_name'] = "Default"
                final_data['last_name'] = "Default"

            request.correct_data = final_data

def get_arrival_and_return_from_segment(segments, departure_airport, arrival_airport):
    last_segment = segments[-1]
    if last_segment['toLocation']['name'] == arrival_airport:   # Cas d'un aller simple
        timestamp = last_segment['endDate']['utcTimestampMillis']
        return datetime.utcfromtimestamp(timestamp/1000), None
    elif last_segment['toLocation']['name'] == departure_airport:  # Cas d'un aller-retour
        timestamp = last_segment['endDate']['utcTimestampMillis']
        return_date = datetime.utcfromtimestamp(timestamp/1000)
        arrival_date = None
        for segment in segments:
            if segment['toLocation']['name'] == arrival_airport:
                timestamp_ar = segment['endDate']['utcTimestampMillis']
                arrival_date = datetime.utcfromtimestamp(timestamp_ar/1000)
        return arrival_date, return_date
    return None, None


def format_segments(segments):
    result = []
    count = 1
    for segment in segments:
        result.append({
            'departure_airport': segment['fromLocation']['name'],
            'departure_country': segment['fromLocation']['countryName'],
            'departure_date_time': datetime.utcfromtimestamp(segment['startDate']['utcTimestampMillis']/1000),
            'arrival_airport': segment['toLocation']['name'],
            'arrival_country': segment['toLocation']['countryName'],
            'arrival_date_time': datetime.utcfromtimestamp(segment['endDate']['utcTimestampMillis']/1000),
            'order': count
        })
        count += 1
    return result
