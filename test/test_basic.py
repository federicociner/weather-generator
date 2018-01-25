from context import src
from src import helpers, generate_data, markov_chain, weather_generator as wg
import unittest
import datetime as dt
import pandas as pd


class TestWeatherGenerator(unittest.TestCase):

    def setUp(self):
        self.start_date = dt.datetime(1990, 1, 1)
        self.end_date = dt.datetime(2017, 12, 31)
        self.histdata = 'historical_data.csv'
        self.geodata = 'geocoded_locations.txt'
        self.obs = 1000
        self.model = wg.WeatherGenerator(
            self.obs, self.start_date, self.end_date, self.histdata, self.geodata)
        self.model.initialize_output()
        self.model.generate_position_data()
        self.model.generate_time_data()
        self.model.generate_weather_data()
        self.model.generate_condition_data()

    def test_numrows(self):
        """Checks whether the number of expected observations, as defined by
        the user, matches the number of rows generated in the final output.
        """
        self.assertEquals(self.model.obs, self.model.output.shape[0])

    def test_maxhumidity(self):
        """Checks that the max value for humidity in the output data frame
        does not exceed 100 (humidity is a relative percentage).
        """
        self.assertLess(self.model.output['Humidity'].max(), 100)

    def test_maxlat(self):
        """Checks that the max value for latitude is less than or equal to
        90 degrees in the geocoded_locations.txt file.
        """
        df = pd.read_csv(helpers.get_datafile(self.geodata))
        self.assertLess(df['Lat'].max(), 90.0)

    def test_minlat(self):
        """Checks that the min value for latitude is greater than or equal to
        -90 degrees in the geocoded_locations.txt file.
        """
        df = pd.read_csv(helpers.get_datafile(self.geodata))
        self.assertGreater(df['Lat'].min(), -90.0)

    def test_maxlng(self):
        """Checks that the max value for longitude is less than or equal to
        180 degrees in the geocoded_locations.txt file.
        """
        df = pd.read_csv(helpers.get_datafile(self.geodata))
        self.assertLess(df['Lng'].max(), 180.0)

    def test_minlng(self):
        """Checks that the min value for longitude is greater than or equal to
        -180 degrees in the geocoded_locations.txt file.
        """
        df = pd.read_csv(helpers.get_datafile(self.geodata))
        self.assertGreater(df['Lng'].min(), -180.0)


if __name__ == '__main__':
    unittest.main()
