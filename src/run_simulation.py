from __future__ import division
import sys
import datetime as dt
from weather_generator import WeatherGenerator
from helpers import save_data
import timeit


if __name__ == '__main__':
    # set variables"
    start_date = dt.datetime(1990, 1, 1)
    end_date = dt.datetime(2017, 12, 31)
    histdata = 'historical_data.csv'
    geodata = 'geocoded_locations.txt'
    obs = int(sys.argv[1])

    # throw error if number of obs is 0 or less
    if obs < 1:
        raise ValueError('Number of observations cannot be less than 1')

    # instantiate new WeatherGenerator object
    weatherGenerator = WeatherGenerator(
        obs, start_date, end_date, histdata, geodata)

    # start timing
    start_time = timeit.default_timer()

    # generate random weather observations
    weatherGenerator.initialize_output()
    weatherGenerator.generate_position_data()
    weatherGenerator.generate_time_data()
    weatherGenerator.generate_weather_data()
    weatherGenerator.generate_condition_data()
    weatherGenerator.order_output()
    output = weatherGenerator.return_output()

    # save data frame to CSV in 'output' directory
    save_data(output, filename='generated_weather_data.csv', subdir='output')

    # stop timing and print elapsed time
    elapsed = str("{:.4f}".format(timeit.default_timer() - start_time))
    print('Generated ' + str(obs) +
          ' random weather observations in ' + elapsed + ' seconds')
