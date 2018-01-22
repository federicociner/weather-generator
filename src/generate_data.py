import pandas as pd
import datetime as dt
import forecastio
import requests
import csv
from helpers import get_filepath


def get_geolocation_data(source, target):
    """Geocodes place names from an input text file using Google Maps API.
    Results are written to a specified target file name.

    Args:
        source (str): Text file name with locations in (City, Country) format.
        target (str): Destination text file name.
    """
    inputfile = open(get_filepath(source), 'r')
    outputfile = csv.writer(open(get_filepath(target), 'w'))
    outputfile.writerow(["location", "lat", "lng"])  # headers

    for row in inputfile:
        row = row.rstrip()
        url = 'http://maps.googleapis.com/maps/api/geocode/json'
        payload = {'address': row, 'sensor': 'false'}
        r = requests.get(url, params=payload)
        json = r.json()

        lat = json['results'][0]['geometry']['location']['lat']
        lng = json['results'][0]['geometry']['location']['lng']

        newrow = [row, lat, lng]
        outputfile.writerow(newrow)


def get_weather_data(locations, start_date, end_date):
    """ Retrieves daily historical weather data for the specified locations
    using the Dark Sky API.

    Args:
        locations (str):
        start_date (datetime.datetime):
        end_date (datetime.datetime)

    Returns:
    """
    locs = get_filepath('geocoded_locations.txt')
    df = pd.read_csv(locs)

    # extract data for each location for date range b/w start and end date
    for index, row in df.iterrows():
        for single_date in daterange(start_date, end_date):
            forecast = forecastio.load_forecast(api_key,
                                                row['lat'],
                                                row['lng'],
                                                time=single_date,
                                                units='si')
            for day in forecast.daily().data:
                print row['location'],day.time, day.temperatureHigh, day.humidity, day.icon, day.dewPoint, day.windBearing