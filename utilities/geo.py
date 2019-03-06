import random


# TODO make this change over time for a more believable demo...
bad_gateway_polygon = [
    [-77.045190, 39.004399], [-77.034190, 39.005399], [-77.003890, 39.000199],
    [-77.018490, 38.983399], [-77.047990, 38.986099], [-77.045190, 39.004399]
]


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
