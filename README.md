# Random Weather Generator

## Description

A random weather data generator written in Python. This program uses the Google Maps API to obtain geopositioning and elevation data for a customised list of locations, as well as the Dark Sky API to obtain historical weather measurements for those locations (e.g. max/min temperature, humidity, pressure). Using these datasets, the generator will create realistic aritifical weather observations in a standard format, and output those observations in a comma-separated values (CSV) file. The data will be output in the following format:

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

### Standard

In order to install the required dependencies and libraries to run the weather generator, your system should have the following prerequisites satisfied:
1. Windows, macOS, and Linux are all supported - however, if you are running Windows you will have to install either Cygwin or WLS (Windows Linux Subsystem) Bash to run the Makefile commands.
1. Python 2.7.12 or greater installed with all standard libraries.
1. Permissions to download and install packages from PyPi via `pip`.

To build the application and download the required Python dependencies, simply clone the repository to your machine/server, `cd` to the project folder (**weather-generator**) and run the `make build` command in Bash. This will download and install all the required dependencies.

### Docker

If you have Docker installed on your system and have an account on DockerHub, you can simply download a lightweight image with all of the project dependencies by running `make dockerbuild` in the main project directory.

## Running a simulation

In order to generate a set of random weather observations, execute `make run obs=<obs>` in the main project direcotry, where the `<obs>` argument is the number of data points you would like to generate in the data set (e.g. `make run obs=1000`).

After running this command, a CSV file named _generated_weather_data.csv_, containing the randomly generated weather observations, will be written to the _output_ folder. **Note:** Any existing datasets in this folder will be overwritten via the make run command.

### Docker

To run an instance of the weather-generator Docker image, simply run `make rundocker` in the project directory - this will start up a Bash session inside the container. From here, you can simply navigate to the project folder via `cd /home/weather-generator` and then execute `make run obs=<obs>` as above.