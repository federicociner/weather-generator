from __future__ import division
import pandas as pd
import datetime as dt
import forecastio
import requests
import csv
import json
import urllib
from helpers import save_data, get_datafile, daterange


def get_geolocation_data(apikey, source, target):
    """Geocodes place names from an input text file using Google Maps API.
    Results are written to a specified target file name.

    Args:
        apikey (str): Google Maps API key.
        source (str): Text file name with locations in (City, Country) format.
        target (str): Destination text file name.

    """
    inputfile = open(get_datafile(source), 'r')
    outputfile = csv.writer(open(get_datafile(target), 'w'))
    outputfile.writerow(['Location', 'Lat', 'Lng', 'Elevation'])  # headers

    for row in inputfile:
        row = row.rstrip()
        url = 'http://maps.googleapis.com/maps/api/geocode/json'
        payload = {'address': row, 'sensor': 'false'}
        r = requests.get(url, params=payload)
        json = r.json()

        lat = json['results'][0]['geometry']['location']['lat']
        lng = json['results'][0]['geometry']['location']['lng']
        elevation = get_elevation(apikey, lat, lng)

        newrow = [row[:row.find(',')], lat, lng, elevation]
        outputfile.writerow(newrow)


def get_elevation(apikey, lat, lng):
    """Gets the elevation for given latitude and longtitude coordinates

    Args:
        apikey (str): Google Maps API key.
        lat (float): Latitude coordinate.
        lng (float): Longitude coordinate.

    """
    url = 'https://maps.googleapis.com/maps/api/elevation/json'
    request = urllib.urlopen(url + '?locations=' +
                             str(lat) + ',' + str(lng) + '&key=' + apikey)
    try:
        results = json.load(request).get('results')
        if 0 < len(results):
            elevation = results[0].get('elevation')
            return elevation
        else:
            print('HTTP GET request failed')
    except ValueError:
        print('JSON decode failed: ' + str(request))


def get_weather_data(apikey, locs, cols, start_date, end_date, offset):
    """ Retrieves daily historical weather data for the specified locations
    using the Dark Sky API. Output is saved as a CSV in the 'data' folder.

    Args:
        api_key (str): Dark Sky API key.
        locs (str): Geocoded locations file name (with extension).
        cols (str): File name contain custom column names.
        start_date (datetime.datetime): Start date for historical data range.
        end_date (datetime.datetime): End date for historical data range.
        offset (int): Step size for iterator (number of days).

    """
    locs_path = get_datafile(locs)
    locs = pd.read_csv(locs_path)

    # get columns list
    columns = get_datafile(cols)
    with open(columns) as f:
        cols = [line.strip() for line in f]

    # extract data for each location for date range b/w start and end date
    tbl = []
    for index, row in locs.iterrows():
        for single_date in daterange(start_date, end_date, offset):
            forecast = forecastio.load_forecast(apikey,
                                                row['Lat'],
                                                row['Lng'],
                                                time=single_date,
                                                units='si')
            h = forecast.daily()
            tz = forecast.json['timezone']
            d = h.data
            for p in d:
                # get date info
                utc = p.d['time']
                dts = dt.datetime.utcfromtimestamp(utc)
                isodate = dt.datetime.utcfromtimestamp(utc).isoformat()
                date_info = [tz, isodate, dts.year, dts.month, dts.day]

                # get location info
                loc, lat, lng = row['Location'], row['Lat'], row['Lng']
                elevation = row['Elevation']
                loc_info = [loc, lat, lng, elevation]

                # get weather attributes - need to handle possible KeyErrors
                temp_high = p.d.get('temperatureHigh', None)
                temp_low = p.d.get('temperatureLow', None)
                humidity = p.d.get('humidity', None) * 100
                pressure = p.d.get('pressure', None)
                attr_info = [temp_high, temp_low, humidity, pressure]
                tbl.append(loc_info + date_info + attr_info)

    # convert output to data frame
    df = pd.DataFrame(tbl)
    df.columns = cols
    filename = 'historical_data.csv'
    save_data(df, filename, sep='|')


def aggregate_data(filename):
    """Aggregates data from historical daily weather observations by location/
    timezone, year, and month.

    Args:
        filename (str): File name of historical weather observations dataset.
    Returns:
        grouped (pandas.DataFrame): Aggregated data set

    """
    path = get_datafile(filename)
    df = pd.read_csv(path, sep='|')

    # get aggregated statistics for humidity, pressure, and temperature
    stats = {'Humidity': [min, max],
             'Pressure': [min, max],
             'TemperatureHigh': 'mean',
             'TemperatureLow': 'mean'}

    # set columns to aggregate data
    group_cols = ['Location', 'Month', 'Timezone']
    grouped = df.groupby(group_cols, as_index=False).aggregate(stats)

    # reset multi-index to single-column labels and shorten column names
    grouped.columns = [''.join(x) for x in grouped.columns.ravel()]
    grouped.rename(columns={'Pressuremin': 'Pmin',
                            'Pressuremax': 'Pmax',
                            'TemperatureHighmean': 'Tmean_high',
                            'TemperatureLowmean': 'Tmean_low',
                            'Humiditymin': 'Hmin',
                            'Humiditymax': 'Hmax'}, inplace=True)

    return grouped
