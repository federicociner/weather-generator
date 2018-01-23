import datetime as dt
import numpy as numpy
import pandas as pd


class WeatherGenerator(object):

    def __init__(self, obs, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.obs = obs

    def random_date(start_date, end_date):
