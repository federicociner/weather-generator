# Random Weather Generator

## Description

A random weather data generator written in Python. This program uses the Google Maps API to obtain geopositioning and elevation data for a customised list of locations, as well as the Dark Sky API to obtain historical weather measurements for those locations (e.g. max/min temperature, humidity, pressure). Using these datasets, the generator will create realistic aritifical weather observations in a standard format, and output those observations in a in comma-separated values (CSV) file. The data will be output in the following format:

Location  | Position         | Local Time          | Conditions | Temperature | Pressure | Humidity
--------- | ---------------- | ------------------- | ---------- | -----------:| --------:| --------:
Sydney    | -33.86,151.21,39 | 2015-12-23 16:02:12 | Rain       |       +12.5 |   1010.3 | 97
Melbourne | -37.83,144.98,7  | 2015-12-25 02:30:55 | Snow       |        -5.3 |    998.4 | 55
Adelaide  | -34.92,138.62,48 | 2016-01-04 23:05:37 | Sunny      |       +39.4 |   1114.1 | 12

where

 - Location is an optional label describing one or more positions
 - Position is a comma-separated triple containing latitude, longitude, and
   elevation in metres above sea level
 - Local time is an ISO8601 datetime
 - Conditions are either 'Snow', 'Rain', or 'Sunny'
 - Temperature is in °C
 - Pressure is in hPa
 - Relative humidity is a %

## Build instructions

## Running a simulation

