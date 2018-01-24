from __future__ import division, absolute_import
import numpy as np
import pandas as pd
from markov_chain import *
from generate_data import *
from helpers import *


class WeatherGenerator(object):
    """Randomly generates a dataset of artificial but realistic weather
    observations, including condition, temperature, humidity and pressure.
    """

    def __init__(self, obs, start_date, end_date, histdata, geodata):
        """Initalise state and class variables.

        Args:
            obs (int): Number of random observations to generate.
            start_date (datetime.datetime): Start date for random date
            generation.
            end_date (datetime.datetime): End date for random date generation.
            histdata (pandas.DataFrame): Historical weather data for selected
            locations aggregated by month and location.
            geodata (pandas.DataFrame): Data set containing geolocation
            information, such as latitude, longitude, and elevation in meters
            above sea level.

        """
        self.start_date = start_date
        self.end_date = end_date
        self.obs = obs
        self.geodata = pd.read_csv(get_datafile(geodata))
        self.histdata = aggregate_data(histdata)
        self.locations = self.histdata['Location'].unique().tolist()
        self.output = None
        self.cols = ['Location', 'Position', 'Local Time',
                     'Conditions', 'Temperature', 'Pressure', 'Humidity']

    def return_output(self):
        """Returns a copy of the output data frame.

        Returns:
            self.output (pandas.DataFrame): Generated weather observations.
        """
        return self.output

    def order_output(self):
        """Orders the output data frame in the correct format.

        """
        self.output = self.output[self.cols]

    def initialize_output(self):
        """Initializes an empty data frame to store randomly generate weather
        observations.

        """
        # set dims and store as 'output' class variable
        rows = self.obs
        dims = len(self.cols)
        self.output = pd.DataFrame(np.zeros((rows, dims)), columns=self.cols)

    def generate_position_data(self):
        """Populates the 'Location' and 'Position' attributes of the output data frame.

        """
        # populate 'Location' field randomly
        self.output['Location'] = np.random.choice(self.locations, self.obs)

        # clean up geodata data frame and create 'Position' attribute
        nc = self.geodata[['Lat', 'Lng', 'Elevation']].round(2)
        nc['Elevation'] = nc['Elevation'].astype(int)
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
        a date range from a randomly selected start date.

        """
        # generate random dates and append to a list
        sd = self.start_date
        ed = self.end_date
        dates = [random_date(start=sd, end=ed) for d in range(0, self.obs)]

        # convert to ISO 8601 format and update "Local Time" field
        self.output['Local Time'] = map(lambda x: x.isoformat(), dates)

    def generate_weather_data(self):
        """Populates the 'Temperature', 'Humidity', and 'Pressure' attributes
        using historical values calculated on a monthly level.

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
        m['Temperature'] = ((m['Tmean_high'] - m['Tmean_low']
                             ) * r + m['Tmean_low']).round(1)
        m['Pressure'] = ((m['Pmax'] - m['Pmin']) * r + m['Pmin']).round(1)
        m['Humidity'] = ((m['Hmax'] - m['Hmin']) * r + m['Hmin']).astype(int)

        # drop redundant columns and assign to output
        dcols = ['Month', 'Timezone', 'Pmax', 'Pmin',
                 'Hmax', 'Hmin', 'Tmean_high', 'Tmean_low']
        m.drop(columns=dcols, inplace=True)
        self.output = m

    def generate_condition_data(self):
        """ Predicts condition ('Sunny', 'Rain', 'Snow') for the next
        observation period using a simple Markov Chain model.

        """
        # set 'Conditions' column to NA
        self.output['Conditions'] = 'NA'

        # instantiate new MarkovChain object
        MC = MarkovChain()

        # apply forecast function on 'Conditions' column based on temperature
        # and humidity values for each observation period
        params = self.output[["Temperature", "Humidity"]]
        self.output[['Conditions']] = params.apply(
            lambda x: MC.forecast_weather(x.values[0], x.values[1]), axis=1)
