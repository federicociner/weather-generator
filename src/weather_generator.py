from __future__ import division, absolute_import
import datetime as dt
import numpy as np
import pandas as pd
from generate_data import *
from helpers import *


class WeatherGenerator(object):
    """Generates a dataset of artificial but realistic weather observations.
    """

    def __init__(self, obs, histdata, geodata):
        self.obs = obs
        self.geodata = pd.read_csv(get_filepath(geodata))
        self.histdata = aggregate_data(histdata)
        self.locations = self.histdata['Location'].unique().tolist()
        self.output = None

    def initialize_output(self):
        """Initializes an empty data frame to store randomly generate weather
        observations.
        """
        cols = ['Location', 'Position', 'Local Time',
                'Conditions', 'Temperature', 'Pressure', 'Humidity']

        # set dims and store as 'output' class variable
        rows = self.obs
        dims = len(cols)
        self.output = pd.DataFrame(np.zeros((rows, dims)), columns=cols)

    def generate_position_data(self):
        """Populates the 'Location' and 'Position' attributes of the output data
        frame.
        """
        # populate 'Location' field randomly
        self.output['Location'] = np.random.choice(self.locations, self.obs)

        # clean up geodata data frame and create 'Position' attribute
        nc = self.geodata[['Lat', 'Lng', 'Elevation']]
        self.geodata['Position'] = nc.astype(
            str).apply(lambda x: ','.join(x), axis=1)
        self.geodata.drop(columns=['Lat', 'Lng', 'Elevation'], inplace=True)

        # update "Position" column in output data frame
        left = self.output.set_index('Location')  # set left index
        right = self.geodata.set_index('Location')  # set right index
        self.output = left.loc[:, left.columns.union(right.columns)]  # union
        self.output.update(right)  # update self.output "Position" column
        self.output.reset_index(inplace=True)

    def generate_time_data(self):
        """Populates the 'Local Time' field sequentially, by location, using
        a date range from a randomly selected start date
        """
        # sort output data frame by location
        self.output.sort_values(['Location'], axis=0, inplace=True)

        # generate random start date and corresponding end date based on obs
        start_date = random_date()
        end_date = start_date + dt.timedelta(days=self.obs)

        # store dates in a list
        dates = [x for x in daterange(start_date, end_date, offset=1)]

        # randomise hour/minute/second precision
        for d in range(0, len(dates)):
            h = random.randint(0, 23)
            m = random.randint(0, 59)
            s = random.randint(0, 59)
            dates[d] = dates[d].replace(hour=h, minute=m, second=s)

        # convert to ISO 8601 format and update "Local Time" field
        self.output['Local Time'] = map(lambda x: x.isoformat(), dates)

    def generate_weather_data(self):
        """Populates the 'Temperature', 'Humidity', and 'Pressure' attributes
        using historical values calculated on a monthly level
        """
        months = pd.to_datetime(self.output['Local Time']).dt.month
        self.output['Month'] = months  # set month values for later joins

        # merge output data frame with historical data to get ranges
        keys = ['Location', 'Month']
        m = pd.merge(self.output, self.histdata, how='left',
                     left_on=keys, right_on=keys)

        # use vectorization to uniformly select random pressure, temperature
        # and humidity values between the historical min and max ranges
        r = np.random.rand(m.shape[0])
        m['Temperature'] = (m['Tmean_high'] - m['Tmean_low']
                            ) * r + m['Tmean_low']
        m['Pressure'] = (m['Pmax'] - m['Pmin']) * r + m['Pmin']
        m['Humidity'] = (m['Hmax'] - m['Hmin']) * r + m['Hmin']

        # drop redundant columns and assign to output
        dcols = ['Month', 'Timezone', 'Pmax', 'Pmin',
                 'Hmax', 'Hmin', 'Tmean_high', 'Tmean_low']
        m.drop(columns=dcols, inplace=True)
        self.output = m
