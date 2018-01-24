from __future__ import division, absolute_import
import sys
import datetime as dt
from generate_data import *
from markov_chain import *
from weather_generator import *


if __name__ == '__main__':
    # set variables"
    start_date = dt.datetime(2012, 1, 1)
    end_date = dt.datetime(2015, 12, 31)
    histdata = 'historical_data.csv'
    geodata = 'geocoded_locations.txt'
    obs = 100

    print("This is the script name: ", sys.argv[0])
    print("This is the number of observations: ", sys.argv[1])

    # instantiate new WeatherGenerator object
    # weatherGenerator = WeatherGenerator(
    #     obs, start_date, end_date, histdata, geodata)
