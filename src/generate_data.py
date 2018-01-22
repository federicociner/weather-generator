from __future__ import division, absolute_import
import pandas as pd
import datetime as dt
import forecastio
import requests
import csv
from helpers import get_filepath, daterange, save_data, timeit


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

        newrow = [row[:row.find(',')], lat, lng]
        outputfile.writerow(newrow)


@timeit
def get_weather_data(api_key, locs, cols, start_date, end_date):
    """ Retrieves hourly historical weather data for the specified locations
    using the Dark Sky API. Output is saved as a CSV in the 'data' folder.

    Args:
        api_key (str): Dark Sky API key.
        locs (str): Geocoded locations file name (with extension).
        cols (str): File name contain custom column names.
        start_date (datetime.datetime): Start date for historical data range.
        end_date (datetime.datetime): End date for historical data range.
    """
    locs_path = get_filepath(locs)
    locs = pd.read_csv(locs_path)

    # get columns list
    columns = get_filepath(cols)
    with open(columns) as f:
        cols = [line.strip() for line in f]

    # extract data for each location for date range b/w start and end date
    for index, row in locs.iterrows():
        tbl = []
        for single_date in daterange(start_date, end_date):
            forecast = forecastio.load_forecast(api_key,
                                                row['lat'],
                                                row['lng'],
                                                time=single_date,
                                                units='si')
            h = forecast.hourly()
            d = h.data
            for p in d:
                # get date info
                utc = p.d['time']
                dts = dt.datetime.utcfromtimestamp(utc)
                isodate = dt.datetime.utcfromtimestamp(utc).isoformat()
                date_info = [isodate, dts.year, dts.month, dts.day, dts.hour]

                # get location info
                loc_info = [row['location'], row['lat'], row['lng']]

                # get weather attributes
                attr_info = [p.d['icon'], p.d['temperature'], p.d['humidity'] * 100, p.d['pressure']]
                tbl.append(loc_info + date_info + attr_info)

        # convert output to data frame
        df = pd.DataFrame(tbl)
        df.columns = cols
        df.name = row['location']
        sd_str = str(start_date.date())
        ed_str = str(end_date.date())
        filename = '_'.join([df.name, sd_str, ed_str]) + '.csv'
        save_data(df, filename, sep='|')


if __name__ == '__main__':
    # generate geocoded locations file
    source = 'locations.txt'
    target = 'geocoded_locations.txt'
    get_geolocation_data(source, target)

    # generate weather data for each location and save as CSV
    api_key = '63ab81b2d8aee963f8e0c22cd4ec4650'
    start_date = dt.datetime(2017, 1, 1)
    end_date = dt.datetime(2017, 1, 3)
    cols = 'columns.txt'
    get_weather_data(api_key, target, cols, start_date, end_date)
