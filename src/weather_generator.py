import datetime as dt
import numpy as numpy
import pandas as pd
from generate_data import *
from helpers import *


class WeatherGenerator(object):

    def __init__(self, start_date, end_date, obs, histdata, geodata):
        self.start_date = start_date
        self.end_date = end_date
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

    def set_geodata(self):
        """Populates the location and position attributes of the output data
        frame.
        """

        # set location
        self.output['Location'] = np.random.choice(self.locations, self.obs)

        # clean up geodata data frame and create "Position" attribute
        concat = self.geodata[['Lat', 'Lng', 'Elevation']]
        self.geodata['Position'] = concat.astype(
            str).apply(lambda x: ','.join(x), axis=1)
        self.geodata = self.geodata[['Location', 'Position']]
