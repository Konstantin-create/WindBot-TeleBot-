from modules.coordinates import *
from modules.windy_forecast import *


def get_weather_from_coords(x, y, donate):
    return get_windy_forecast(x, y, donate)


def get_weather_from_city(name, donate):
    x, y = get_coords(name)
    return get_windy_forecast(x, y, donate)
