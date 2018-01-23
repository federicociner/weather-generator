from generate_data import *
from weather_generator import *

if __name__ == '__main__':
    # set variables"
    ds_api_key = '63ab81b2d8aee963f8e0c22cd4ec4650'
    maps_api_key = 'AIzaSyDDNWV2QqV_SdygOs3A7ucVs-LNaL-PiUI'
    source = 'locations.txt'
    target = 'geocoded_locations.txt'

    get_geolocation_data(maps_api_key, source, target)
