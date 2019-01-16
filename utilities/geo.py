import random


def frange(start, stop, step, precision=5):
    while start < stop:
        yield int(start * 10**precision) / 10**precision
        start += step


def random_dc_point():
    lat = random.choice(list(frange(38.7, 39.1, .0001)))
    lon = random.choice(list(frange(-77.3, -76.8, .0001)))
    return lon, lat


def random_bad_gateway_point():
    lat = random.choice(list(frange(38.987999, 39.002999, .0001)))
    lon = random.choice(list(frange(-77.044990, -77.020990, .0001)))
    return lon, lat
